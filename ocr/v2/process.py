from typing import List

import cv2
import numpy as np
from easyocr import Reader

from ocr.base_ocr import BaseOCR
from ocr.libs.normalize_text import NormalizeText


class ProcessOCRV2(BaseOCR):
    instance = None

    @staticmethod
    def get_instance():
        if not ProcessOCRV2.instance:
            ProcessOCRV2.instance = ProcessOCRV2()
        return ProcessOCRV2.instance

    def __init__(self):
        self.angle_rotation: float = None
        self.data: dict = {}
        super().__init__()

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        # Cavet
        detector: Reader = self.easyocr.get("en")
        # predictor: Predictor = self.vietocr
        try:
            image = cv2.imread(self.image_upload)
            image = np.array(image)
            if self.template_data.mode == 2:
                easy_ocr_res = detector.readtext(image,
                                                min_size = 5,
                                                text_threshold = 0.7,
                                                link_threshold = 0.4,
                                                mag_ratio = 2.,
                                                slope_ths = 0.3,
                                                height_ths = 0.5,
                                                width_ths = 0.3)
                templates = self.template_data.template
                res = self.get_amount(easy_ocr_res, templates)
                return res
            return {}
        except:
            return {}

    def get_amount(self, easy_ocr_res: list, templates: dict):
        for key, lst_field in templates.items():
            lst_field: List[str]
            for field in lst_field:
                for i in range(len(easy_ocr_res) - 1):
                    _, text1, _ = easy_ocr_res[i]
                    _, text2, _ = easy_ocr_res[i+1]
                    text1: str = text1.upper()
                    text2: str = text2.upper()
                    text = text1 + " " + text2
                    field = field.upper()
                    if field in text1 and not isinstance(templates[key], str):
                        if key == "amount":
                            if NormalizeText.normalize_amount(text1) != 0:
                                templates[key] = NormalizeText.normalize_amount(text1)
                            elif NormalizeText.normalize_amount(text) != 0:
                                templates[key] = NormalizeText.normalize_amount(text)
                        elif key == "date":
                            if NormalizeText.normalize_date(text1) != "":
                                templates[key] = NormalizeText.normalize_date(text1)
                            elif NormalizeText.normalize_date(text) != "":
                                templates[key] = NormalizeText.normalize_date(text)
                        elif key == "time":
                            if NormalizeText.normalize_time(text1) != "":
                                templates[key] = NormalizeText.normalize_time(text1)
                            elif NormalizeText.normalize_time(text) != "":
                                templates[key] = NormalizeText.normalize_time(text)
                        else:
                            templates[key] = text

                if isinstance(templates[key], str):
                    easy_ocr_res.pop(i+1)
                    easy_ocr_res.pop(i)
                    break

        for key, res in templates.items():
            if not isinstance(res, str):
                templates[key] = ""

        return templates
