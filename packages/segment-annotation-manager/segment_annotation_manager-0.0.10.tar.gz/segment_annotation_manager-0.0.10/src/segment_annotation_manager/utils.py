from .environment import Environment
import shapely
import random
import shutil
import cv2
import os


class Utils(Environment):
    ####################################################################################
    # Annotations
    ####################################################################################
    @staticmethod
    def get_xy_coordinates(segment):
        return segment[::2], segment[1::2]

    @staticmethod
    def get_polygon_coordinates(x, y):
        return sum(map(list, zip(x, y)), [])

    @staticmethod
    def make_polygon_from_segment(segment):
        x, y = Utils.get_xy_coordinates(segment)
        polygon = shapely.Polygon(list(zip(x, y)))
        return polygon

    @staticmethod
    def make_segment_from_polygon(polygon):
        xy = polygon.exterior.xy
        x, y = list(xy[0]), list(xy[1])
        return Utils.get_polygon_coordinates(x, y)

    @staticmethod
    def simplify_polygon(segment, tolerance):
        polygon = Utils.make_polygon_from_segment(segment)
        simplified_poly = polygon.simplify(tolerance)
        simplified_seg = Utils.make_segment_from_polygon(simplified_poly)
        # print(len(segment), len(simplified_seg))
        return simplified_seg

    ####################################################################################
    # Datasets
    ####################################################################################
    @staticmethod
    def getFrames(videoDirPath: str, dstDirPath: str):
        """Extract frames (as .PNG) from video"""

        count = 0
        for video in os.listdir(videoDirPath):
            # Convert to open-cv video object
            vidcap = cv2.VideoCapture(f'{videoDirPath}/{video}')
            vidcap.set(cv2.CAP_PROP_ORIENTATION_AUTO, 1)
            success, image = vidcap.read()

            # Save the frame as a .PNG with the CVAT image naming system
            while success:
                cv2.imwrite(f'{dstDirPath}/frame_{str(count).zfill(6)}.PNG', image)
                success, image = vidcap.read()
                print('Read a new frame: ', success)
                count += 1

    def save_random_sample(self, num):
        images = os.listdir(self.IMAGES_DIR)
        sample = random.sample(images, num)

        dest_dir = os.path.join(self.DATA_DIR, 'sampled_images')
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)

        for image in sample:
            image_path = os.path.join(self.IMAGES_DIR, image)
            dest_path = os.path.join(dest_dir, image)
            shutil.copy(image_path, dest_path)

