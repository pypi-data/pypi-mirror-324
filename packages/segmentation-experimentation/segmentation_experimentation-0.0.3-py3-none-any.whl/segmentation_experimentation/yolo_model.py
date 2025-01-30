from segment_annotation_manager.dataset import Dataset
from segment_annotation_manager.config import Config
from segment_annotation_manager.environment import Environment
from .logger import Logger
from ultralytics import YOLO
from ultralytics.data.annotator import auto_annotate
import os
import shutil


class Model(Environment):
    """
    The Model class contains the main functions necessary to train a YOLO model and use it for predictions.
    """
    def __init__(self, **kwargs):
        # Sets configuration from file
        self.file = kwargs.get('file', self.CONFIG_PATH)
        self.config = Config(file=self.file)

        # Remove cache if specified
        remove_cache = kwargs.get('remove_cache', False)
        if remove_cache:
            settings_path = r"C:\Users\Alexander\AppData\Roaming\Ultralytics\settings.json"
            if os.path.exists(settings_path):
                os.remove(settings_path)

        # Sets logger
        self.logger = kwargs.get('logger', Logger())

        # Gets project name
        self.name = self.config.name

        # Prepares dataset for training
        self.dataset = Dataset(self.config)
        self.dataset.prepare()
        self.dataset.preprocess_images()

    def train(self, **kwargs):
        """Train the model on the processed dataset using custom parameters"""
        name = kwargs.get('name', self.name)

        self.logger.log()
        self.logger.experiment.set_name(name)
        self.logger.experiment.log_parameters(self.config.training_parameters)

        # Train model
        model = YOLO(os.path.join(self.WEIGHTS_DIR, 'yolo11m-seg.pt'), task='segment')
        model.train(name=name, data=self.CONFIG_PATH, **self.config.training_parameters)

        # Delete augmented images
        self.dataset.delete_augmented_images()

    def tune(self, **kwargs):
        name = kwargs.get('name', self.name)

        model = YOLO(os.path.join(self.WEIGHTS_DIR, 'yolo11m-seg.pt'))
        model.tune(data=self.CONFIG_PATH, epochs=200, iterations=300, optimizer='AdamW')

    def export(self, **kwargs):
        """Export the .pt model into a different format. Options are engine (TensorRT), onnx, or openvino."""
        # Get name and format
        name = kwargs.get('name', self.name)
        format = kwargs.get('format', self.config.training_parameters['format'])

        # Export to specified format
        model = YOLO(os.path.join(self.RUNS_DIR, rf'train\{name}\weights\best.pt'), task='segment')
        model.export(format=format)

    def val(self, **kwargs):

        # Get name and format
        name = kwargs.get('name', self.name)
        modelType = kwargs.get('format', self.config.training_parameters['format'])

        # Predict instances
        model = YOLO(os.path.join(self.RUNS_DIR, rf'train\{name}\weights\best.{modelType}'), task='segment')
        model.val(data=self.file, device=0, split='train', save_json=True, save_hybrid=True)
        pass

        # Move predictions under runs\predict\name
        val_path = os.path.join(self.RUNS_DIR, 'validate')
        if not os.path.exists(val_path):
            os.mkdir(val_path)
        os.rename(os.path.join(self.RUNS_DIR, r'segment\val'), os.path.join(val_path, name))
        shutil.rmtree(os.path.join(self.RUNS_DIR, r'segment'))

    def predict(self, **kwargs):
        """Predict instances using pre-trained YOLO model"""
        name = kwargs.get('name', self.name)

        # Get images to run predictions on
        imageDir = kwargs.get('imageDir', self.IMAGES_DIR)
        images = os.listdir(imageDir)

        # Get model type
        modelType = kwargs.get('format', self.config.training_parameters['format'])

        # Predict instances
        model = YOLO(os.path.join(self.RUNS_DIR, rf'train\{name}\weights\best.{modelType}'), task='segment')
        try:
            results = model(source=[os.path.join(imageDir, x) for x in images],
                            **self.config.predict_parameters)
        except AssertionError:
            for image in images:
                results = model(source=os.path.join(imageDir, image), **self.config.predict_parameters)

        # Move predictions under runs\predict\name
        predict_path = os.path.join(self.RUNS_DIR, 'predict')
        if not os.path.exists(predict_path):
            os.mkdir(predict_path)
        os.rename(os.path.join(self.RUNS_DIR, r'segment\predict'), os.path.join(predict_path, name))
        shutil.rmtree(os.path.join(self.RUNS_DIR, r'segment'))

        self.dataset.process_prediction_labels()

    def auto_annotate(self, **kwargs):
        """Predict instances of each class and create labels containing mask coordinates"""
        name = kwargs.get('name', self.name)

        # Get images to run predictions on
        imageDir = kwargs.get('imageDir', self.IMAGES_DIR)

        # Get model type
        modelType = kwargs.get('format', self.config.training_parameters['format'])

        # Run auto annotation function if auto annotations do not already exist
        annotate_dir = os.path.join(self.RUNS_DIR, rf'annotate')
        if not os.path.exists(annotate_dir):
            os.mkdir(annotate_dir)
        if not os.path.exists(os.path.join(annotate_dir, name)):
            auto_annotate(data=imageDir,
                          det_model=os.path.join(self.RUNS_DIR, rf'train\{name}\weights\best.pt'),
                          sam_model=os.path.join(self.WEIGHTS_DIR, 'sam_b.pt'),
                          output_dir=os.path.join(annotate_dir, name),
                          device='0')
        else:
            print('Auto annotations already created')

        # Process auto annotations
        self.dataset.process_auto_annotation_results(name)

    def evaluate(self):
        pass
