import os
import warnings

from django.apps import AppConfig

from base.utils import load_env


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        warnings.filterwarnings("ignore")
        print("Loading environment ...")
        load_env()

        if os.environ.get('RUN_MAIN'):
            print("Loading model ...")
            from ocr.libs.load_model import LoadModel
            load_model = LoadModel()
            load_model.download()

            from ocr.v1.process import ProcessOCRV1
            ProcessOCRV1.get_instance()

            from ocr.v2.process import ProcessOCRV2
            ProcessOCRV2.get_instance()
