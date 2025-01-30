import pandas
from segment_annotation_manager.config import Config
from segment_annotation_manager.environment import Environment
from .yolo_model import Model
from itertools import combinations, product
import pandas as pd
import numpy as np
import yaml
import time
import os


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

        self.time_df = pd.DataFrame(columns=['name', 'training_time', 'export_time'])

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
            output_dir = kwargs.get('outputDir', self.EXPERIMENTS_DIR)
            config_path = os.path.join(output_dir, self.exp_name)
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
                                predict_parameters={'conf': 0.75, 'max_det': len(self.categories), 'save': True,
                                                    'save_txt': True, 'classes': list(range(0, len(self.categories)))},
                                config_dir=config_path)

            config.generate(name='config', categories=self.categories,
                            training_parameters={'format': 'engine', 'epochs': 500, 'verbose': True,
                                                 'optimizer': 'SGD', 'plots': True, 'profile': True},
                            predict_parameters={'conf': 0.75, 'max_det': len(self.categories), 'save': True,
                                                'save_txt': True, 'classes': list(range(0, len(self.categories)))})

    def run(self, **kwargs):
        configs_dir = kwargs.get('configsDir', os.path.join(self.EXPERIMENTS_DIR, self.exp_name))

        for config in os.listdir(configs_dir):
            start_time = time.time()

            model = Model(file=os.path.join(configs_dir, config))
            model.train()

            end_time = time.time()
            training_time = end_time - start_time

            start_time = time.time()
            model.export()
            end_time = time.time()
            export_time = end_time - start_time

            self.time_df.loc[len(self.time_df)] = {'name': model.name,
                                                   'training_time': training_time,
                                                   'export_time': export_time}

    def collect_raw_data(self):
        trials = os.listdir(self.PREDICT_DIR)

        data = []  # name, time, best epoch, fitness
        for trial in trials:
            trial_dir = os.path.join(self.PREDICT_DIR, trial)
            results_path = os.path.join(trial_dir, 'results.csv')

            results = pd.read_csv(results_path)
            # epoch,time,train/box_loss,train/seg_loss,train/cls_loss,train/dfl_loss,metrics/precision(B),
            # metrics/recall(B),metrics/mAP50(B),metrics/mAP50-95(B),metrics/precision(M),metrics/recall(M),
            # metrics/mAP50(M),metrics/mAP50-95(M),val/box_loss,val/seg_loss,val/cls_loss,val/dfl_loss,lr/pg0,
            # lr/pg1,lr/pg2

            results['fitness(B)'] = 0.1 * results['metrics/mAP50(B)'] + 0.9 * results['metrics/mAP50-95(B)']
            results['fitness(M)'] = 0.1 * results['metrics/mAP50(M)'] + 0.9 * results['metrics/mAP50-95(M)']

            best_b = results.loc[results['fitness(M)'].idxmax()]
            best_m = results.loc[results['fitness(M)'].idxmax()]

            print(f'Best Box Fitness: {best_b}')
            print(f'Best Mask Fitness: {best_m}')
            print(f'Time (results vs. python): {results.loc[-1]["time"]} {self.time_df.loc[self.time_df["name" == trial]]["training_time"]}')

            data.append([trial, results.loc[-1]["time"], best_m['epoch'], best_m['fitness(M)']])

        columns = ['name', 'time', 'best_epoch', 'fitness']
        data_dict = [dict(zip(columns, row)) for row in data]
        raw_df = pandas.DataFrame(data=data_dict)
        raw_df.to_csv(self.PREDICT_DIR, index=False)


