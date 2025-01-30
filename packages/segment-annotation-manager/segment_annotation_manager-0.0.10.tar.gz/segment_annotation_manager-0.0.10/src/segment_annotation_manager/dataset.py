from .environment import Environment
from .annotation import Annotation
from .config import Config
from .utils import Utils
import cv2
import shutil
import os


class Dataset(Environment):
    """
    A Dataset class prepares the various data types for training by the Model object. It contains multiple Annotation
    objects and their corresponding images and categories.
    """

    def __init__(self, datasetConfig: Config):
        # Define data lists
        self.videos = []
        self.images = []
        self.categories = []

        # Define annotations
        self.original_annotations = Annotation()
        self.augmented_annotations = Annotation()
        self.predicted_annotations = Annotation(reference_annotation=self.original_annotations)
        self.auto_annotations = Annotation(reference_annotation=self.original_annotations)
        self.merged_annotations = Annotation(reference_annotation=self.original_annotations)

        # Set the configuration
        self.config = datasetConfig

    def prepare(self, overwrite=False):
        """Converts the data into formats usable by the YOLO model"""

        # Get frames from video if necessary
        if len(os.listdir(self.VIDEOS_DIR)) > 0:
            # Make the image directory
            if not os.path.exists(self.IMAGES_DIR):
                os.mkdir(self.IMAGES_DIR)
            # Get frames
            if len(os.listdir(self.IMAGES_DIR)) == 0 or overwrite:
                self.clean(images=True)
                Utils.getFrames(self.VIDEOS_DIR, self.IMAGES_DIR)

        # Combine annotation files from multiple videos into one file
        if 'v2.json' in os.listdir(self.COCO_ANNOTATIONS_DIR):
            self.combine_video_annotations()

        # Update original annotations object
        self.original_annotations.load_from_COCO_json(config=self.config)

        # Convert COCO format to YOLO format and split dateset if necessary
        if not os.path.exists(self.YOLO_DATASET_DIR) or overwrite:
            self.clean(yolo_dataset=True)
            self.original_annotations.split_annotations()

    def preprocess_images(self, **kwargs):

        def grey(img):
            # Convert image to greyscale
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        def hist_eq(img):
            # Histogram equalization
            if len(img.shape) == 2:
                # Account for greyscale images
                return cv2.equalizeHist(img)

            # Equalize Y channel of color images
            img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
            img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            eq = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            return eq

        def median_blur(img):
            # Apply median blur
            return cv2.medianBlur(img, 7)

        def Gaussian_blur(img):
            # Apply Gaussian blur
            return cv2.GaussianBlur(img, (5, 5), 0)

        def bilateral_filter(img):
            # Apply bilateral filter
            return cv2.bilateralFilter(img, 9, 150, 150)

        if 'Image Preprocessing' not in self.config.config.keys():
            return

        imageDir = kwargs.get('imageDir', os.path.join(self.YOLO_DATASET_DIR, r'train\images'))

        preprocessing_dict = {
            'grey': grey,
            'hist_eq': hist_eq,
            'med_blur': median_blur,
            'Gaus_blur': Gaussian_blur,
            'bi_filter': bilateral_filter,
        }

        preprocessing_steps = self.config.config['Image Preprocessing']

        for image in os.listdir(imageDir):
            imagePath = os.path.join(imageDir, image)
            img = cv2.imread(imagePath)

            # Assemble preprocessing pipeline
            for step in preprocessing_steps:
                res = preprocessing_dict[step](img)
                img = res

            cv2.imwrite(imagePath, img)

    def delete_augmented_images(self, **kwargs):
        images_dir = kwargs.get('imageDir', self.IMAGES_DIR)

        # Search for augmented images in images directory
        images = os.listdir(images_dir)
        for image in images:
            # Delete augmented images
            if 'aug' in image:
                image_path = os.path.join(images_dir, image)
                os.remove(image_path)

    def process_prediction_results(self, results):
        self.predicted_annotations.load_from_results(results=results)
        self.predicted_annotations.export_to_YOLO_label()

    def process_prediction_labels(self, **kwargs):
        name = kwargs.get('name', self.config.name)

        # Load annotations into Annotation object from a YOLO labels directory. Must add a reference annotation to get
        # image and class data, as they are not available in the YOLO label format.
        self.predicted_annotations.batch_load_from_YOLO_dir(os.path.join(self.RUNS_DIR, rf"predict\{name}\labels"))

        # Merge the original annotations with the predicted annotations, preserving the original annotations
        self.merged_annotations = self.original_annotations.merge(self.predicted_annotations, config=self.config)

        # Simplify annotations by removing points along same line
        self.merged_annotations.simplify_segments(tolerance=1.25)

        # Save auto annotations to JSON if they do not already exist
        if not os.path.exists(self.AUTO_ANNOTATIONS_DIR):
            os.mkdir(self.AUTO_ANNOTATIONS_DIR)
            self.merged_annotations.export_to_COCO_json(os.path.join(
                self.AUTO_ANNOTATIONS_DIR, 'simplified_merged_annotations.json'))

        self.merged_annotations.calculate_metrics(name=name)

    def process_auto_annotation_results(self, name: str):
        """Converts the results of the auto annotation function into a format usable by CVAT.
        Also simplifies the annotations so they contain fewer points and are easier to work with. """

        # Load annotations into Annotation object from a YOLO labels directory. Must add a reference annotation to get
        # image and class data, as they are not available in the YOLO label format.
        self.auto_annotations.batch_load_from_YOLO_dir(os.path.join(self.RUNS_DIR, rf"annotate\{name}"))

        # Merge the original annotations with the auto annotations, preserving the original annotations
        self.merged_annotations = self.original_annotations.merge(self.auto_annotations, config=self.config)

        # TODO: Add functionality to snap annotations together
        # self.merged_annotations.snap_segments('Pulmonary Artery', 'Aorta')

        # Simplify annotations by removing points along same line
        self.merged_annotations.simplify_segments(tolerance=1.5)

        # Save auto annotations to JSON if they do not already exist
        if not os.path.exists(self.AUTO_ANNOTATIONS_DIR):
            os.mkdir(self.AUTO_ANNOTATIONS_DIR)
            self.merged_annotations.export_to_COCO_json(os.path.join(
                self.AUTO_ANNOTATIONS_DIR, 'simplified_merged_annotations.json'))

    def clean(self, yolo_dataset=True, images=False, videos=False, original_annotations=False,
              auto_annotations=True):
        """Removes old data"""

        if yolo_dataset and os.path.exists(self.YOLO_DATASET_DIR):
            shutil.rmtree(self.YOLO_DATASET_DIR)

        if auto_annotations and os.path.exists(self.AUTO_ANNOTATIONS_DIR):
            shutil.rmtree(self.AUTO_ANNOTATIONS_DIR)

        if images and os.path.exists(self.IMAGES_DIR):
            shutil.rmtree(self.IMAGES_DIR)
            os.mkdir(self.IMAGES_DIR)

        if videos:
            shutil.rmtree(self.VIDEOS_DIR)
            os.mkdir(self.VIDEOS_DIR)

        if original_annotations:
            shutil.rmtree(self.COCO_ANNOTATIONS_DIR)
            os.mkdir(self.COCO_ANNOTATIONS_DIR)

    def combine_video_annotations(self, **kwargs):
        annotations_dir = kwargs.get('annotationsDir', self.COCO_ANNOTATIONS_DIR)

        annotation_files = []
        for file in os.listdir(annotations_dir):
            if 'v' in file:
                annotation_files.append(os.path.join(annotations_dir, file))

        annotation_files.sort()

        combined_annotation = Annotation()
        frame_addend, annotation_id = 0, 1
        for file in annotation_files:
            temp_annotation = Annotation()
            temp_annotation.load_from_COCO_json(annotationFile=file)

            for category in temp_annotation.categories:
                if category.name not in [x.name for x in combined_annotation.categories]:
                    combined_annotation.categories.append(category)

            for image in temp_annotation.images:
                new_image_id = int(image.id) + frame_addend
                new_image_name = f'frame_{str(new_image_id - 1).zfill(6)}.PNG'

                image.id = new_image_id
                image.file_name = new_image_name

                if image.id not in [x.id for x in combined_annotation.images]:
                    combined_annotation.images.append(image)

            for annotation in temp_annotation.annotations:
                annotation.image_id += frame_addend
                annotation.id = annotation_id
                combined_annotation.annotations.append(annotation)
                annotation_id += 1

            frame_addend += len(temp_annotation.images)

        combined_annotation.export_to_COCO_json(os.path.join(annotations_dir, 'instances_default.json'))

    def split_video_annotations(self, **kwargs):
        video_dir = kwargs.get('videosDir', self.VIDEOS_DIR)
        annotation_path = kwargs.get('annotationFile', self.COCO_ANNOTATIONS_PATH)

        frame_dict = {}
        vid_num = 1
        for video in sorted(os.listdir(video_dir)):
            # Convert to open-cv video object
            vidcap = cv2.VideoCapture(f'{video_dir}/{video}')
            success, image = vidcap.read()

            count = 0
            while success:
                success, image = vidcap.read()
                count += 1

            frame_dict[vid_num] = count

            vid_num += 1

        combined_annotation = Annotation()
        combined_annotation.load_from_COCO_json(annotationFile=annotation_path)
        # combined_annotation.display()

        annotations = []
        current_frame = 0
        for key, value in frame_dict.items():
            temp_annotation = Annotation()

            temp_annotation.categories.extend(combined_annotation.categories)

            for image in combined_annotation.images:
                if (image.id <= value + current_frame) and (image.id > current_frame):
                    new_image_id = image.id - current_frame
                    new_image_name = f'frame_{str(new_image_id - 1).zfill(6)}.PNG'
                    image.id = new_image_id
                    image.file_name = new_image_name
                    temp_annotation.images.append(image)

            for annotation in combined_annotation.annotations:
                if (annotation.image_id - current_frame <= value) and annotation.image_id - current_frame > 0:
                    annotation.image_id -= current_frame
                    temp_annotation.annotations.append(annotation)

            annotations.append(temp_annotation)
            current_frame += value

        for annotation in annotations:
            annotation.display()
            annotation.export_to_COCO_json(fileName=os.path.join(
                self.AUTO_ANNOTATIONS_DIR, f'v{str(annotations.index(annotation) + 1)}.json'))
