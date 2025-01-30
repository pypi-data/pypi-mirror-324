from segment_annotation_manager.environment import Environment
import comet_ml
import os
# from tensorboardX import SummaryWriter


class Logger(Environment):
    def __init__(self, **kwargs):
        api_file_path = kwargs.get('api_file', os.path.join(os.getcwd(), 'comet_api_key'))
        self.api_key = kwargs.get('api_key', open(api_file_path, 'r').read())

        os.environ["COMET_LOG_GIT_METADATA"] = "false"
        os.environ["COMET_LOG_CONDA_PACKAGES"] = "false"
        os.environ["COMET_LOG_CONDA_ENV"] = "false"

        comet_ml.login(project_name='heart', directory=r'logs', api_key=self.api_key)

        # writer = SummaryWriter(comet_config={"disabled": False})
        # self.experiment = comet_ml.Experiment(api_key='5v4st7d33CRZrTX9DKRyMqB07')

        # tb = program.TensorBoard()
        # tb.configure(argv=[None, '--logdir', os.path.join(self.RUNS_DIR, 'train')])
        # url = tb.launch()

    def log(self):
        self.experiment = comet_ml.Experiment(api_key=self.api_key)
        # writer = tf.summary.create_file_writer(r'runs\logs')

