from .data_objects import Category, Image, SegmentAnnotation
from .environment import Environment
from .config import Config
from .utils import Utils
from ultralytics.utils.ops import segments2boxes
from shapely.ops import snap
from shapely.geometry import Point, Polygon
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import random
import json
import shutil
import os
import numpy as np
import math
import cv2


class Annotation(Environment):
    """
    The Annotation class handles the annotations on a set of images. These annotations can be in either the COCO JSON
    format or the YOLO txt format.

    An Annotation object consists of a list of files, images, categories, and annotations.
    """

    def __init__(self, **kwargs):
        # Load from reference annotation if provided
        reference_annotation = kwargs.get('reference_annotation', False)

        if not reference_annotation:
            # Initialize an empty Annotation object
            self.files = kwargs.get('files', [])
            self.images = kwargs.get('images', [])
            self.categories = kwargs.get('categories', [])

        else:
            # Take files, images, and categories from reference annotation
            self.files = reference_annotation.files
            self.images = reference_annotation.images
            self.categories = reference_annotation.categories

        self.annotations = kwargs.get('annotations', [])

    ####################################################################################
    # Load or export annotations
    ####################################################################################
    def load_from_COCO_json(self, **kwargs):
        """Create Annotation object containing a list of Categories, Images, and SegmentAnnotations from a
        COCO JSON file"""

        # Get and load annotations file
        annotationFile = kwargs.get('annotationFile', self.COCO_ANNOTATIONS_PATH)
        annotation = json.load(open(annotationFile))
        self.files.append(annotationFile)

        # Add categories
        for category in annotation['categories']:
            catObj = Category(name=category['name'],
                              category_id=category['id'])
            self.categories.append(catObj)

        # Add images
        for image in annotation['images']:
            imageObj = Image(file_name=image['file_name'],
                             image_id=image['id'],
                             width=image['width'],
                             height=image['height'])
            self.images.append(imageObj)

        # Get which classes of the JSON annotation to load from the config file
        config = kwargs.get('config', Config())
        keep_images, drop_images, keep_categories, drop_categories = config.update(self, 'train')

        # Add annotations
        for a in annotation['annotations']:
            # Edit attributes dictionary, or create one if it does not exist
            try:
                a['attributes']['format'] = 'COCO'
            except KeyError:
                a['attributes'] = {'format': 'COCO'}

            # Get the category name from its id
            category_name = self.get_category(category_id=a['category_id']).name

            # Create the SegmentAnnotation object using the various data
            aObj = SegmentAnnotation(annotation_id=a['id'],
                                     image_id=a['image_id'],
                                     category_id=a['category_id'],
                                     bbox=a['bbox'],
                                     area=a['area'],
                                     segmentation=a['segmentation'][0],
                                     attributes=a['attributes'])

            # Add to annotations if specified in config
            if (a['image_id'] in keep_images and a['image_id'] not in drop_images) and (
                    category_name in keep_categories and category_name not in drop_categories):
                self.annotations.append(aObj)

    def export_to_COCO_json(self, fileName):
        """Exports Annotation objects into the COCO JSON format"""

        # Create data dictionary
        data = {
            'categories': [{'id': c.id, 'name': c.name, 'supercategory': c.supercategory}
                           for c in self.categories],
            'images': [{'id': i.id, 'file_name': i.file_name, 'width': i.width, 'height': i.height}
                       for i in self.images],
            'annotations': [{'id': a.annotation_id, 'image_id': a.image_id, 'category_id': a.category_id,
                             'area': a.area, 'bbox': [np.float64(x) for x in a.bbox], 'segmentation': [a.segmentation],
                             'iscrowd': 0, 'attributes': a.attributes}
                            for a in self.annotations]
        }

        # Write to file
        with open(fileName, 'w') as f:
            json.dump(data, f)

    def load_from_YOLO_label(self, labelSource: str, **kwargs):
        """Create Annotation object containing a list of Categories, Images, and SegmentAnnotations from a
        YOLO label file. NOTE: image and category data are usually not present, so a reference Annotation object or a
        list of class and image objects must be passed in"""

        # Check if reference was made in init
        if len(self.categories) == 0 and len(self.images) == 0:
            # Get reference categories and images
            categories = kwargs.get('categories', [])
            images = kwargs.get('images', [])
            if categories == [] and images == []:
                reference_annotation = kwargs.get('reference_annotation', Annotation())
                categories = reference_annotation.categories
                images = reference_annotation.images
        else:
            categories = self.categories
            images = self.images

        # Get label file or label string
        if os.path.exists(labelSource):
            # Add and read file
            self.files.append(labelSource)
            label = open(labelSource).readlines()

            # Add image
            image_name = f"{os.path.basename(labelSource).split('.')[0]}.PNG"

        else:
            # Read from a string
            label = labelSource.split('\n')
            image_name = kwargs.get('file_name', 'frame_000000.PNG')

        image = self.get_image(file_name=image_name, image_list=images)
        if image.id not in [x.id for x in self.images]:
            self.images.append(image)

        # Add annotation
        for annotation in label:
            # Add category
            category_id = int(annotation.split(' ')[0]) + 1
            category = self.get_category(category_id=category_id, category_list=categories)
            if category not in self.categories:
                self.categories.append(category)

            # Create segment from normalized x and y coordinates
            xn, yn = annotation.split(' ')[1::2], annotation.split(' ')[2::2]
            x = [round(float(a) * image.width, 2) for a in xn]
            y = [round(float(a) * image.height, 2) for a in yn]
            segment = Utils.get_polygon_coordinates(x, y)

            # Calculate the bounding box of the segment
            try:
                seg = np.array([list(a) for a in list(zip(x, y))])
                seg.reshape(-1, 2)
                bbox = segments2boxes([seg])[0]
            except ValueError:
                print('ValueError: not enough values to unpack (expected 2, got 0):', image.id)
                bbox = 0

            # Calculate the area of the segment
            # print(image.id, segment)
            if len(segment) < 4:
                continue

            poly = Utils.make_polygon_from_segment(segment)
            area = poly.area

            # Get the annotation id
            a = (image.id * random.randint(50, 100)) ** category.id + 1
            b = math.log10(abs(a))
            c = a / (category.id * b)
            d = math.log10(c / (image.id ** category.id))
            e = round(d % 1, 8) * (10 ** 8)
            annotation_id = int(e)

            # Create SegmentAnnotation object using various data
            aObj = SegmentAnnotation(annotation_id=annotation_id,
                                     image_id=image.id,
                                     category_id=category.id,
                                     bbox=bbox,
                                     area=area,
                                     segmentation=segment,
                                     attributes={'format': 'YOLO'})

            # Add annotation
            self.annotations.append(aObj)

    def batch_load_from_YOLO_dir(self, labelDir: str, **kwargs):
        """Add YOLO annotations to Annotation object from a directory containing multiple label files"""

        # Get reference data
        categories = kwargs.get('categories', [])
        images = kwargs.get('images', [])
        reference_annotation = kwargs.get('reference_annotation', Annotation())

        # Get label files in directory
        labels = os.listdir(labelDir)
        for label in labels:
            # Load annotation
            self.load_from_YOLO_label(labelSource=os.path.join(labelDir, label), categories=categories, images=images,
                                      reference_annotation=reference_annotation)

    def export_to_YOLO_label(self, **kwargs):
        """Exports Annotation objects into multiple YOLO label formats"""

        # Get directories
        inputDir = kwargs.get('inputDir', self.IMAGES_DIR)
        outputDir = kwargs.get('outputDir', self.YOLO_ANNOTATIONS_DIR)
        IMAGES_DIR = os.path.join(outputDir, 'images')
        LABELS_DIR = os.path.join(outputDir, 'labels')

        # Make directories if they do not exist
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        if not os.path.exists(IMAGES_DIR):
            os.mkdir(IMAGES_DIR)
            os.mkdir(LABELS_DIR)

        # Get images as each YOLO file is organized by image
        images = kwargs.get('images', self.images)
        for image in images:
            # Get annotations corresponding to image
            annotations = self.get_annotations(image_id=image.id)

            # Skip unannotated images
            if len(annotations) == 0:
                continue

            # Set variable for file contents
            yoloOutput = []
            for annotation in annotations:
                # Convert segment into normalized x and y stream
                x, y = annotation.x, annotation.y
                xn, yn = [a / image.width for a in x], [b / image.height for b in y]
                poly = Utils.get_polygon_coordinates(xn, yn)

                # Combine category id with segment to form one line of the file
                line = [annotation.category_id - 1, *[round(x, 6) for x in poly]]
                yoloOutput.append(' '.join([str(x) for x in line]))

            # Create the file contents
            yoloString = '\n'.join(yoloOutput)

            # Write to the file
            f = open(os.path.join(LABELS_DIR, f"{image.file_name.split('.')[0]}.txt"), 'w')
            f.write(yoloString)
            f.close()

            # Copy the corresponding image into the directory
            shutil.copy(os.path.join(inputDir, image.file_name), IMAGES_DIR)

    def load_from_iPad_photos(self, show=False, **kwargs):
        """
        Load an Annotation object from folders containing images with certain classes annotated using Photos Markup.
        Each annotation must be for one instance of each category. Each category should be separated by a subdirectory.
        """

        # Set the initial configuration
        config = Config()
        category_list = config.categories

        # Get annotations directory
        annotations_dir = kwargs.get('annotationsDir', self.IPAD_ANNOTATIONS_DIR)

        # Cycle through each category present in the directory
        for category in os.listdir(annotations_dir):
            # Get information about the category
            cat_path = os.path.join(annotations_dir, category)
            cat_id = category_list.index(category) + 1
            cat_obj = Category(name=category, category_id=cat_id)

            # Add the category to the list of categories for the current annotation
            self.categories.append(cat_obj)

            # Cycle through each image
            for image in os.listdir(cat_path):
                # Read the image
                image_path = os.path.join(cat_path, image)
                img = cv2.imread(image_path)

                # Get information about the image
                base_name = image.split('.')[0]
                file_name = f'{base_name}.PNG'
                image_id = int(base_name.split('_')[1]) + 1

                # Create and append image object to current Annotation
                img_obj = Image(file_name=file_name,
                                image_id=image_id,
                                width=img.shape[1], height=img.shape[0])
                if img_obj.id not in [x.id for x in self.images]:
                    self.images.append(img_obj)

                # Isolate bright green color from image and create contours
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, np.array((40, 150, 150)), np.array((65, 255, 255)))
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Select largest contour
                max_contour, max_coords, max_length = [], [], 0
                for cnt in contours:
                    # Flatten array of contours of shape (N, 1, 2) into a list of (x, y) coordinate tuples
                    coords = [(point[0][0], point[0][1]) for point in cnt]

                    # Set to max if greater than current
                    if len(coords) > max_length:
                        max_coords = coords
                        max_contour = cnt
                        max_length = len(coords)

                # Create a Shapely polygon from the contour coordinates
                try:
                    poly = Polygon(max_coords)
                    seg = Utils.make_segment_from_polygon(poly)
                    poly = Utils.make_polygon_from_segment(Utils.simplify_polygon(seg, 1.5))
                except ValueError:
                    print(f'{category} {image} {max_coords}')
                    cv2.imshow('mask', mask)
                    cv2.waitKey(0)

                if show:
                    cv2.imshow('image', img)
                    cv2.imshow('mask', mask)
                    cv2.waitKey(0)

                # Check if the polygon is valid
                if poly.is_valid and not poly.is_empty:
                    # Create SegmentAnnotation object
                    annotation_obj = SegmentAnnotation(
                        annotation_id=0,
                        image_id=image_id,
                        category_id=cat_id,
                        bbox=cv2.boundingRect(max_contour),
                        area=poly.area,
                        segmentation=Utils.make_segment_from_polygon(poly),
                        attributes={'source': 'iPad'}
                    )

                    self.annotations.append(annotation_obj)

    def export_to_iPad_photos(self):
        if not os.path.exists(self.AUTO_ANNOTATIONS_DIR):
            os.mkdir(self.AUTO_ANNOTATIONS_DIR)

        for annotation in self.annotations:
            image_id = annotation.image_id
            image_name = self.get_image(image_id=image_id).file_name

            img = cv2.imread(os.path.join(self.ORIGINAL_IMAGES_DIR, image_name))
            poly = Utils.make_polygon_from_segment(annotation.segmentation)
            coords = list(poly.exterior.coords)
            pts = np.array(coords, dtype=np.int32).reshape((-1, 1, 2))

            cv2.polylines(
                img,
                [pts],
                isClosed=True,
                color=(0, 255, 0),
                thickness=4
            )

            category_id = annotation.category_id
            category_name = self.get_category(category_id=category_id).name
            category_dir = os.path.join(self.AUTO_ANNOTATIONS_DIR, category_name)

            if not os.path.exists(category_dir):
                os.mkdir(category_dir)

            cv2.imwrite(os.path.join(category_dir, image_name), img)

    def load_from_results(self, results, **kwargs):

        # Check if reference was made in init
        if len(self.categories) == 0 and len(self.images) == 0:
            reference_annotation = kwargs.get('reference_annotation', Annotation())
            self.categories = reference_annotation.categories
            self.images = reference_annotation.images

        for result in results:
            boxes = result.boxes
            category_ids = [int(x) for x in boxes.cls.tolist()]
            file_name = os.path.basename(result.path)
            masks = result.masks.xy

            yoloOutput = []
            for i in range(0, len(category_ids)):
                # Combine category id with segment to form one line of the file
                if len(masks[i]) != 0:
                    line = [category_ids[i]]
                    line.extend([val for sublist in masks[i] for val in sublist])
                    yoloOutput.append(' '.join([str(x) for x in line]))

            labelString = '\n'.join(yoloOutput)

            if len(yoloOutput) > 5:
                self.load_from_YOLO_label(labelSource=labelString, file_name=file_name)

    ####################################################################################
    # Retrieve object using identifier
    ####################################################################################
    def get_image(self, image_id=None, file_name=None, **kwargs) -> Image:
        """Get image from id or file name"""

        image_list = kwargs.get('image_list', self.images)
        for image in image_list:
            if image.id == image_id:
                return image
            elif image.file_name == file_name:
                return image
        return None

    def get_category(self, category_id=None, category_name=None, **kwargs) -> Category:
        """Get category from id or category name"""

        category_list = kwargs.get('category_list', self.categories)
        for category in category_list:
            if category.id == category_id:
                return category
            elif category.name == category_name:
                return category
        return None

    def get_annotation(self, image_id=None, category_id=None, image_name=None, category_name=None) \
            -> SegmentAnnotation:
        """Get single annotation from image id and category id"""

        # Convert names into ids
        if image_name is not None:
            image_id = self.get_image(file_name=image_name).id
        if category_name is not None:
            category_id = self.get_category(category_name=category_name).id

        for annotation in self.annotations:
            if annotation.image_id == image_id and annotation.category_id == category_id:
                return annotation
        return None

    def get_annotations(self, image_id=None, category_id=None, image_name=None, category_name=None) \
            -> [SegmentAnnotation]:
        """Get all annotations from image id or category id"""

        # Convert names into ids
        if image_name is not None:
            image_id = self.get_image(file_name=image_name).id
        if category_name is not None:
            category_id = self.get_category(category_name=category_name).id

        annotations = []
        for annotation in self.annotations:
            if annotation.image_id == image_id:
                annotations.append(annotation)
            if annotation.category_id == category_id:
                annotations.append(annotation)

        return annotations

    ####################################################################################
    # Modify annotations
    ####################################################################################
    def merge(self, new_annotation, **kwargs):
        """Merge two Annotation objects, reusing class and image data from the base annotation.
        Annotations from base annotation will not be overwritten by new annotation"""

        # Get which classes of the new annotation to merge from the config file
        config = kwargs.get('config', Config())
        _, _, keep, drop = config.update(self, 'merge')

        transferred_categories = []
        for category in self.categories:
            if category.name in keep and category.name not in drop:
                transferred_categories.append(category.name)

        # Add unique annotations to list of base annotations
        merged_annotations = self.annotations.copy()
        for annotation in new_annotation.annotations:
            existing_annotation = self.get_annotation(image_id=annotation.image_id,
                                                      category_id=annotation.category_id)

            if existing_annotation is None:
                merged_annotations.append(annotation)

        # Add unique images to list of base images
        merged_images = self.images.copy()
        for image in new_annotation.images:
            if self.get_image(image_id=image.id) is None:
                merged_images.append(image)

        # Make new annotation object with new annotations, and images and categories from base annotation
        merged_annotation = Annotation(files=list({*self.files, *new_annotation.files}),
                                       images=merged_images,
                                       categories=self.categories,
                                       annotations=merged_annotations)

        return merged_annotation

    def drop(self, image_ids=None, category_ids=None, image_names=None, category_names=None):
        """Drop annotations from certain images or containing certain frames"""

        dropped_annotations = []

        if image_ids is not None:
            for image_id in image_ids:
                dropped_annotations.extend(self.get_annotations(image_id=image_id))

        if category_ids is not None:
            for category_id in category_ids:
                dropped_annotations.extend(self.get_annotations(category_id=category_id))

        if image_names is not None:
            for image_name in image_names:
                dropped_annotations.extend(self.get_annotations(image_name=image_name))

        if category_names is not None:
            for category_name in category_names:
                dropped_annotations.extend(self.get_annotations(category_name=category_name))

        for annotation in dropped_annotations:
            self.annotations.remove(annotation)

    def edit_categories(self, category_list):
        current_categories = self.categories
        current_category_dict = {x.id: x.name for x in current_categories}

        for annotation in self.annotations:
            old_category_id = annotation.category_id
            category_name = current_category_dict[old_category_id]

            try:
                new_category_id = category_list.index(category_name) + 1
                annotation.category_id = new_category_id
            except ValueError:
                self.annotations.remove(annotation)

        new_categories = []
        for category_name in category_list:
            new_category_id = category_list.index(category_name) + 1

            if category_name not in current_category_dict.values():
                category = Category(name=category_name, category_id=new_category_id)
            else:
                category = self.get_category(category_name=category_name)
                category.id = new_category_id

            new_categories.append(category)

        self.categories = new_categories

    def split_annotations(self, split=(0.80, 0.20, 0.0)):
        """Split images and annotations into train, val, and test directories"""

        # Set directory paths
        TRAIN_DIR = os.path.join(self.YOLO_DATASET_DIR, 'train')
        VAL_DIR = os.path.join(self.YOLO_DATASET_DIR, 'val')
        TEST_DIR = os.path.join(self.YOLO_DATASET_DIR, 'test')

        # Create directories if they do not exist
        if not os.path.exists(self.YOLO_DATASET_DIR):
            os.makedirs(TRAIN_DIR)
            os.makedirs(VAL_DIR)
            os.makedirs(TEST_DIR)

        # Get augmented images
        aug_images = []
        for image in self.images.copy():
            if len(self.get_annotations(image_name=image.file_name)) > 0:
                if 'aug' in image.file_name:
                    aug_images.append(image)

        # Calculate percentage of aug images and new split
        aug_percent = len(aug_images) / len(self.images)
        if aug_percent != 0:
            revised_split = (split[0] - aug_percent, split[1], split[2])
            remaining = sum(revised_split)
            split = (revised_split[0] / remaining, revised_split[1] / remaining, revised_split[2] / remaining)

        # Get images
        image_list = []
        for image in self.images.copy():
            if len(self.get_annotations(image_name=image.file_name)) > 0:
                if 'aug' not in image.file_name:
                    image_list.append(image)

        # Get training images
        train_images = random.sample(image_list, int(split[0] * len(image_list)))
        train_images.extend(aug_images)
        self.export_to_YOLO_label(outputDir=TRAIN_DIR, images=train_images)

        # Get validation images
        new_ratio = round(split[1] / (1 - split[0]), 2)
        for x in train_images.copy():
            if x in image_list:
                image_list.remove(x)
        val_images = random.sample(image_list, int(new_ratio * len(image_list)))
        self.export_to_YOLO_label(outputDir=VAL_DIR, images=val_images)

        # Get testing images
        new_ratio = split[-1] / (1 - split[0] - split[1])
        for x in val_images: image_list.remove(x)
        test_images = random.sample(image_list, int(new_ratio * len(image_list)))
        self.export_to_YOLO_label(outputDir=TEST_DIR, images=test_images)

    def simplify_segments(self, tolerance: float):
        """Simplify segments by removing similar points"""
        for annotation in self.annotations:
            annotation.segmentation = Utils.simplify_polygon(annotation.segmentation, tolerance)

    def snap_segments(self, base_category, edit_category):
        """Snap segments to one another if they are bordering"""
        # TODO: Not currently working
        base_category_ID = self.get_category(category_name=base_category).id
        edit_category_ID = self.get_category(category_name=edit_category).id

        for image in self.images:
            image_id = image.id
            base_annotation = self.get_annotation(image_id=image_id, category_id=base_category_ID)
            edit_annotation = self.get_annotation(image_id=image_id, category_id=edit_category_ID)

            base_poly = Utils.make_polygon_from_segment(base_annotation.segmentation)
            edit_poly = Utils.make_polygon_from_segment(edit_annotation.segmentation)

            edit_points = gpd.GeoSeries([Point(x, y) for x, y in edit_poly.exterior.coords])
            distances = edit_points.distance(base_poly)

            edit_annotation.segmentation = Utils.make_segment_from_polygon(snap(base_poly, edit_poly, 0.5))

    ####################################################################################
    # Area calculations
    ####################################################################################
    def calculate_metrics(self, name):
        data, loaded_images = [], {}
        for annotation in self.annotations:
            # Get segment annotation
            poly = Utils.make_polygon_from_segment(annotation.segmentation)

            # Convert to contour
            exterior_coords = list(poly.exterior.coords)  # (x, y) shape
            coords_array = np.array(exterior_coords, dtype=np.float32)
            cnt = coords_array.reshape((-1, 1, 2))  # (N, 1, 2) shape

            # Get area
            area = cv2.contourArea(cnt)

            # Get perimeter
            perimeter = cv2.arcLength(cnt, True)

            # Get centroid from moments
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # Get aspect ratio (width / height)
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h

            # Get extent (fullness of contour in comparison to bounding rectangle)
            rect_area = w * h
            extent = float(area) / rect_area

            # Get solidity (fullness of contour in comparison to convex hull)
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            solidity = float(area) / hull_area

            # Get the equivalent diameter, which is the diameter of the circle whose area is same as the contour area
            equi_diameter = np.sqrt(4 * area / np.pi)

            # Get the angle at which the object is directed
            (x, y), (MA, ma), angle = cv2.fitEllipse(cnt)

            # Get the mean value of the image mask within the contour
            # Load image if not in loaded_images dictionary
            if annotation.image_id not in list(loaded_images.keys()):
                image_obj = self.get_image(image_id=annotation.image_id)
                image_path = os.path.join(self.IMAGES_DIR, image_obj.file_name)
                image = cv2.imread(image_path)
                loaded_images[annotation.image_id] = image
            else:
                image = loaded_images[annotation.image_id]
            # Create mask and find mean value
            mask = np.zeros(image.shape[:2], np.uint8)
            mean_val = cv2.mean(image, mask=mask)

            # Get locations of extreme values
            leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
            rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
            topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
            bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])

            # Add to data
            data.append([annotation.annotation_id, annotation.image_id, annotation.category_id, area, perimeter,
                         (cx, cy), aspect_ratio, extent, solidity, equi_diameter, angle, bottommost, topmost, mean_val])

        # Create and export dataframe
        columns = ['Annotation ID', 'Image ID', 'Category ID', 'Area', 'Perimeter', 'Centroid', 'Aspect Ratio',
                   'Extent', 'Solidity', 'Equivelent Diameter', 'Orientation', 'Minimum Location', 'Maximum Location',
                   'Mean Color']
        df = pd.DataFrame(columns=columns, data=data)
        df = df.sort_values(by=['Image ID', 'Category ID'])
        df.to_csv(os.path.join(self.PREDICT_DIR, name, 'calculations.csv'), index=False)

    def get_mask_areas(self, categories: [Category]) -> [[float]]:
        """Returns the areas of the masks per specified category"""

        areas = []
        for category in categories:
            category_areas = []
            for annotation in self.annotations:
                category_name = self.get_category(category_id=annotation.category_id).name
                if category_name == category:
                    category_areas.append(annotation.area)
            areas.append(category_areas)
        return areas

    def get_bbox_wh_ratio(self, categories: [Category]) -> [[float]]:
        """Returns the ratios of the width and height of the bounding boxes per specified category"""
        ratios = []
        for category in categories:
            category_ratios = []
            for annotation in self.annotations:
                category_name = self.get_category(category_id=annotation.category_id).name
                if category_name == category:
                    bbox = annotation.bbox
                    wh = bbox[-2] / bbox[-1]
                    category_ratios.append(wh)
            ratios.append(category_ratios)
        return ratios

    def get_frames_at_peaks(self, data: [float], plot=False, makeFolder=False):
        """Saves the images where data is at a local maximum"""

        # Get peaks in data and corresponding image ids
        peaks, _ = find_peaks(data, distance=17)
        image_ids = [x + 1 for x in peaks]

        # Get Image objects
        peak_images = []
        for image in self.images:
            if image.id in image_ids:
                peak_images.append(image)

        # Plot peaks if specified
        if plot:
            plt.plot(data)
            plt.plot(peaks, [data[peak] for peak in peaks], "x")
            plt.show()

        # Save images to folder if specified
        if makeFolder:
            peak_path = os.path.join(self.DATA_DIR, 'peak_images')
            os.mkdir(peak_path)
            for image in peak_images:
                image_path = os.path.join(self.IMAGES_DIR, image.file_name)
                shutil.copy(image_path, peak_path)

    ####################################################################################
    # Display
    ####################################################################################
    def display(self):
        """Print information about Annotation object"""
        print(f'Images: {len(self.images)}')
        print(f'\t{", ".join([str(x.id) for x in self.images])}')
        print(f'\nAnnotated Images: {len(set([x.image_id for x in self.annotations]))}')
        print(f'\t{", ".join([str(y) for y in sorted(list(set([x.image_id for x in self.annotations])))])}')
        print(f'\nNumber of Annotations: {len(self.annotations)}')
        print(f'\tExpected Number: {len(self.categories) * len(set([x.image_id for x in self.annotations]))}')
        print(f'\nCategories: {len(self.categories)}')
        print(f'\t{", ".join([f"{x.name} ({x.id})" for x in self.categories])}')

        annotation = random.choice(self.annotations)
        print(f'\nRandom Annotation: {annotation.annotation_id}')
        print(f'\tImage: {self.get_image(annotation.image_id).file_name} ({annotation.image_id})')
        print(f'\tCategory: {self.get_category(annotation.category_id).name} ({annotation.category_id})')
        print(f'\tSegment Length: {len(annotation.segmentation)}')
        print(f'\tBounding Box: {", ".join([str(x) for x in list(annotation.bbox)])}')
        print(f'\tArea: {annotation.area}')

    def query(self, image_id=None, category_id=None, image_name=None, category_name=None):
        """Display information about annotations at a certain image or of a certain category"""
        if image_name is not None:
            image_id = self.get_image(file_name=image_name).id
        if category_name is not None:
            category_id = self.get_category(category_name=category_name).id

        annotations = []
        for annotation in self.annotations:
            if image_id is not None and category_id is not None:
                if annotation.image_id == image_id and annotation.category_id == category_id:
                    annotations.append(annotation)
            else:
                if annotation.image_id == image_id:
                    annotations.append(annotation)
                if annotation.category_id == category_id:
                    annotations.append(annotation)

        for annotation in annotations:
            print(f'\nAnnotation: {annotation.annotation_id}')
            print(f'\tImage: {self.get_image(annotation.image_id).file_name} ({annotation.image_id})')
            print(f'\tCategory: {self.get_category(annotation.category_id).name} ({annotation.category_id})')
            print(f'\tSegment Length: {len(annotation.segmentation)}')
            print(f'\tBounding Box: {", ".join([str(x) for x in list(annotation.bbox)])}')
            print(f'\tArea: {annotation.area}')
