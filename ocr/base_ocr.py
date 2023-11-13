from functools import lru_cache
from typing import Dict
import json
from django.conf import settings
from easyocr import Reader
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor

from api.models.template import TemplateModel
from api.response.template import TemplateData
from ocr.libs.utils import *


class BaseOCR:
    #Singleton Pattern
    instance = None

    @staticmethod
    def get_instance():
        if not BaseOCR.instance:
            BaseOCR.instance = BaseOCR()
        return BaseOCR.instance
    #-----------------#

    def __init__(self):
        self.image_upload: str = ''
        self.image_ocr: str = ''
        self.template_data: TemplateData = {}
        self.gpu: bool = get_device()
        self.easyocr: dict = self.__easyocr()
        self.vietocr: Predictor = self.__vietocr()

    def __call__(self, template_id: int, image_upload: str) -> None:
        # Reset data
        self.image_upload: str = ''
        self.image_ocr: str = ''
        self.template_data: TemplateData = {}
        # Update data
        try:
            template_data = TemplateModel.objects.get(template_id=template_id)
        except:
            raise ValueError(f"TemplateModel has not template_id={template_id}")
        self.image_upload = image_upload
        self.template_data = TemplateData(**template_data.__dict__)

    @lru_cache
    def __easyocr(self) -> Dict[str, Reader]:
        languages = get_languages()
        reader = {}
        for language in languages:
            reader[language] = Reader(lang_list=[language], gpu=self.gpu, verbose=False)
        return reader

    @lru_cache
    def __vietocr(self) -> Predictor:
        config = Cfg.load_config_from_name('vgg_seq2seq')
        config['cnn']['pretrained']=False
        config['predictor']['beamsearch']=False
        config['weights'] = settings.MODEL['vietocr']['filepath']
        if self.gpu:
            config['device'] = 'cuda:0'
        else:
            config['device'] = 'cpu'
        detector = Predictor(config)
        return detector

    def _crop(self):
        pass

    def _rotate(self):
        pass

    def _auto_correct(self):
        pass

    def _normalize_text(self):
        pass
