from .utils import *


class Category(object):
    def __init__(self, name, category_id, supercategory=''):
        self.name = name
        self.id = category_id
        self.supercategory = supercategory


class Image(object):
    def __init__(self, file_name, image_id, width, height):
        self.file_name = file_name
        self.id = image_id
        self.width = width
        self.height = height


class AugmentedImage(Image):
    def __init__(self, file_name, image_id, width, height):
        super().__init__(file_name, image_id, width, height)
        self.file_name = file_name
        self.id = image_id
        self.width = width
        self.height = height


class SegmentAnnotation(object):
    def __init__(self, annotation_id, image_id, category_id, bbox, area, segmentation, attributes):
        self.annotation_id = annotation_id
        self.image_id = image_id
        self.category_id = category_id
        self.bbox = bbox
        self.area = area
        self.segmentation = segmentation
        self.attributes = attributes

        self.x, self.y = Utils.get_xy_coordinates(self.segmentation)
