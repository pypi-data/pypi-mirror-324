from .environment import Environment
from .data_objects import Image, Category
import yaml
import os


class Config(Environment):
    """
    The Config class stores configuration data. It reads in a configuration file and updates the base configuration.
    """
    def __init__(self, **kwargs):
        # Load base config and config files
        self.config = yaml.load(open(kwargs.get('file', self.CONFIG_PATH)), yaml.Loader)
        self.baseConfig = yaml.load(open(self.BASE_CONFIG_PATH), yaml.Loader)

        # Set training, predict, and dataset parameters
        for key, value in self.config['Training Parameters'].items():
            self.baseConfig['Training Parameters'][key] = value
        for key, value in self.config['Predict Parameters'].items():
            self.baseConfig['Predict Parameters'][key] = value
        for key, value in self.config['Dataset Parameters'].items():
            for key2, value2 in self.config['Dataset Parameters'][key].items():
                for key3, value3 in self.config['Dataset Parameters'][key][key2].items():
                    self.baseConfig['Dataset Parameters'][key][key2][key3] = value3

        # Get initial and merge data
        self.LoadInitialAnnotations = self.baseConfig['Dataset Parameters']['LoadInitialAnnotations']
        self.MergeAutoAnnotations = self.baseConfig['Dataset Parameters']['MergeAutoAnnotations']

        data_obj_modifications = [self.LoadInitialAnnotations, self.MergeAutoAnnotations]
        # Loop through stages
        for stage in data_obj_modifications:
            # Loop through the possible data objects
            for obj in ['Images', 'Categories']:
                # Check if data object in configuration
                if obj in stage:
                    # Get list of modifications to data object
                    mods = list(stage[obj].keys())
                    # Loop through list of possible modifications
                    for mod in ['keep', 'drop']:
                        # Check if mod in configuration
                        if mod in mods:
                            kd = stage[obj][mod]
                            # Process image and category keep/drop input
                            if type(kd) is str and kd != 'all':
                                kd_processed = []
                                groups = kd.split(', ')
                                for group in groups:
                                    num_range = [int(x) for x in group.split('-')]
                                    kd_processed.extend(list(range(num_range[0], num_range[1] + 1)))
                                kd = kd_processed

                            stage[obj][mod] = kd

        self.training_parameters = self.baseConfig['Training Parameters']
        self.predict_parameters = self.baseConfig['Predict Parameters']
        self.dataset_parameters = self.baseConfig['Dataset Parameters']

        # Set other values
        for key, value in self.config.items():
            if key not in ['Training Parameters', 'Predict Parameters', 'Dataset Parameters']:
                self.baseConfig[key] = value

        self.categories = self.baseConfig['names']
        self.name = self.baseConfig['name']

    def update(self, annotationObj, stage: str) -> [[Image], [Image], [Category], [Category]]:
        """Updates Image and Category objects in an Annotation object depending on the dataset configuration"""

        lia, maa = self.dataset_parameters['LoadInitialAnnotations'], self.dataset_parameters['MergeAutoAnnotations']
        for mod in [lia['Images'], maa['Images']]:
            if mod['keep'] == 'all':
                mod['keep'] = [x.id for x in annotationObj.images]
        for mod in [lia['Categories'], maa['Categories']]:
            if mod['keep'] == 'all':
                mod['keep'] = [x.name for x in annotationObj.categories]

        if stage == 'train':
            drop_images = lia['Images']['drop']
            keep_images = lia['Images']['keep']

            drop_categories = lia['Categories']['drop']
            keep_categories = lia['Categories']['keep']
        else:
            drop_images = maa['Images']['drop']
            keep_images = maa['Images']['keep']

            drop_categories = maa['Categories']['drop']
            keep_categories = maa['Categories']['keep']

        return keep_images, drop_images, keep_categories, drop_categories

    def generate(self, name, **kwargs):
        config_dir = kwargs.get('config_dir', self.CONFIGS_DIR)

        dataset_path = kwargs.get('dataset_path', os.path.join(os.getcwd(), 'data', 'yolo_dataset'))
        train_path = kwargs.get('train_path', r'train\images')
        val_path = kwargs.get('val_path', r'val\images')
        test_path = kwargs.get('test_path', r'test\images')

        categories = kwargs.get('categories', [])
        nc = len(categories)

        image_preprocessing = kwargs.get('image_preprocessing', [])
        image_augmentation = kwargs.get('image_augmentation', [])

        training_parameters = kwargs.get('training_parameters', {})
        predict_parameters = kwargs.get('predict_parameters', {})
        dataset_parameters = kwargs.get('dataset_parameters', {})

        if dataset_parameters == {}:
            dataset_parameters = {'LoadInitialAnnotations': {'Images': {'keep': 'all'}, 'Categories': {'drop': []}},
                                  'MergeAutoAnnotations': {'Categories': {'keep': 'all'}}}

        contents = {'path': dataset_path, 'train': train_path, 'val': val_path, 'test': test_path,
                    'names': categories, 'nc': nc, 'name': name,
                    'Image Preprocessing': image_preprocessing, 'Image Augmentation': image_augmentation,
                    'Training Parameters': training_parameters, 'Predict Parameters': predict_parameters,
                    'Dataset Parameters': dataset_parameters}

        with open(os.path.join(config_dir, f'{name}.yaml'), 'w') as f:
            yaml.dump({'path': dataset_path}, f, default_flow_style=False)
            yaml.dump({'train': train_path, 'val': val_path, 'test': test_path}, f, default_flow_style=False)
            f.write('\n')
            yaml.dump({'names': categories, 'nc': nc, 'name': name}, f, default_flow_style=False)
            f.write('\n')
            yaml.dump({'Image Preprocessing': image_preprocessing}, f, default_flow_style=False)
            f.write('\n')
            yaml.dump({'Image Augmentation': image_augmentation}, f, default_flow_style=False)
            f.write('\n')
            yaml.dump({'Training Parameters': training_parameters}, f, default_flow_style=False)
            f.write('\n')
            yaml.dump({'Predict Parameters': predict_parameters}, f, default_flow_style=False)
            f.write('\n')
            yaml.dump({'Dataset Parameters': dataset_parameters}, f, default_flow_style=False)

        # config.generate(name='test', categories=['test1', 'test2'], image_preprocessing=['hist_eq'],
        #                 training_parameters={'format': 'engine', 'epochs': 500, 'verbose': True,
        #                                      'optimizer': 'SGD', 'plots': True, 'profile': True},
        #                 predict_parameters={'conf': 0.5, 'max_det': 6, 'save': True, 'save_txt': True,
        #                                     'classes': list(range(0, 2))})
