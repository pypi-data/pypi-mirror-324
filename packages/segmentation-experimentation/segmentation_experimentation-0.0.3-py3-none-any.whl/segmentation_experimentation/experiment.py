from segment_annotation_manager.config import Config
from segment_annotation_manager.environment import Environment
from .yolo_model import Model
from itertools import combinations, product
import os
import yaml
import numpy as np


class Experiment(Environment):
    def __init__(self, **kwargs):
        config_path = kwargs.get('exp_config', os.path.join(self.EXPERIMENTS_DIR, 'exp1.yaml'))

        if kwargs.get('exp_config', True):
            self.config = yaml.load(open(config_path), yaml.Loader)
            self.exp_name = self.config['exp_name']
            self.categories = self.config['categories']
            self.variables = self.config['variables']
            self.max_trials = self.config['max_trials']

        else:
            self.exp_name = kwargs.get('exp_name', 'exp')
            self.categories = kwargs.get('categories', ['test1', 'test2'])
            self.variables = kwargs.get('variables', {})
            self.max_trials = kwargs.get('max_trials', 50)

    def prepare_samples(self, **kwargs):
        var_names = list(self.variables.keys())
        blank_var_dict = {'options': [], 'num_per_trial': 0}

        augmentation = self.variables['augmentation'] if 'augmentation' in var_names else blank_var_dict
        preprocessing = self.variables['preprocessing'] if 'preprocessing' in var_names else blank_var_dict

        combs = {}
        for param in self.variables['training_params']:
            options = self.variables['training_params'][param]
            if isinstance(options, tuple):
                if len(options) == 2:
                    options = list(options)
                    options[2] = 1
                options = [float(x) for x in np.arange(options[0], options[1] + options[2], options[2])]
                param = param.replace('_range', '')
            combs[param] = options

        aug_options = augmentation['options']
        aug_comb_num = augmentation['num_per_trial'] if 'num_per_trial' in augmentation else 1
        aug_combs = [list(x) for x in combinations(aug_options, aug_comb_num)]
        if len(aug_combs[0]) != 0:
            combs['augmentation'] = aug_combs

        prep_options = preprocessing['options']
        prep_comb_num = preprocessing['num_per_trial'] if 'num_per_trial' in preprocessing else 1
        prep_combs = [list(x) for x in combinations(prep_options, prep_comb_num)]
        if len(prep_combs[0]) != 0:
            combs['preprocessing'] = prep_combs

        keys = combs.keys()
        values = combs.values()
        final_combs = [dict(zip(keys, comb)) for comb in product(*values)]

        cont = input(f'The configuration calls for {len(final_combs) + 1}. Would you like to continue? ')
        if cont in ['y', 'yes', '']:
            config_path = os.path.join(self.EXPERIMENTS_DIR, self.exp_name)
            if not os.path.exists(config_path):
                os.mkdir(config_path)

            config = Config()
            for combo in final_combs:
                name = ''
                name += f'aug_{"-".join(combo["augmentation"])}_' if 'augmentation' in combo else ''
                name += f'prep_{"-".join(combo["preprocessing"])}_' if 'preprocessing' in combo else ''

                aug = combo['augmentation'] if 'augmentation' in combo else []
                prep = combo['preprocessing'] if 'preprocessing' in combo else []
                if 'augmentation' in combo:
                    del combo['augmentation']
                if 'preprocessing' in combo:
                    del combo['preprocessing']

                for param in list(combo.keys()):
                    name += f'{param}-{combo[param]}_'

                name = name[:-1]
                name = name.replace('hist_eq', 'eq')
                name = name.replace('Gaus_blur', 'gaus')
                name = name.replace('bi_filter', 'bi')
                name = name.replace('optimizer', 'opt')

                # print(name)

                config.generate(name=name, categories=self.categories,
                                image_preprocessing=prep, image_augmentation=aug,
                                training_parameters={'format': 'engine', 'epochs': 500, 'verbose': True,
                                                     'plots': True, **combo},
                                predict_parameters={'conf': 0.75, 'max_det': 6, 'save': True, 'save_txt': True,
                                                    'classes': list(range(0, len(self.categories)))},
                                config_dir=config_path)

    # def run(self):
