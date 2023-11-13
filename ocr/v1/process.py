import cv2
import numpy as np
from easyocr import Reader
from vietocr.tool.predictor import Predictor
from ocr.base_ocr import BaseOCR
from ocr.libs.image_processing import ImageProcessing
from ocr.libs.normalize_text import NormalizeText
from ocr.libs.mapping import Mapping
from ocr.libs.utils import horizontal_to_rect, perspective_transform
from PIL import Image

class ProcessOCRV1(BaseOCR):
    instance = None

    @staticmethod
    def get_instance():
        if not ProcessOCRV1.instance:
            ProcessOCRV1.instance = ProcessOCRV1()
        return ProcessOCRV1.instance

    def __init__(self):
        self.angle_rotation: float = None
        self.data: dict = {}
        super().__init__()

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        # Cavet
        detector: Reader = self.easyocr.get("en")
        predictor: Predictor = self.vietocr
        try:
            image = cv2.imread(self.image_upload)
            image = np.array(image)
            if self.template_data.mode == 1:
                horizontal_list, free_list = detector.detect(image,
                                                                min_size = 5,
                                                                text_threshold = 0.7,
                                                                link_threshold = 0.4,
                                                                mag_ratio = 2.,
                                                                slope_ths = 0.3,
                                                                height_ths = 0.1,
                                                                width_ths = 0.1)
                horizontal_list, free_list = horizontal_list[0], free_list[0]
                shift_x, shift_y, crop_size_h, crop_size_w = perspective_transform(horizontal_list)
                rect_from_horizontal = [horizontal_to_rect(box) for box in horizontal_list]
                template = self.template_data.box
                template = ImageProcessing.format_rect_template(template, crop_size_h, crop_size_w, shift_x, shift_y)
                template, rect_group = Mapping.format_template(template)
                if rect_group:
                    image_group = np.zeros(image.shape, np.uint8)
                    for rect in rect_group:
                        image_rect = ImageProcessing.crop_group_object_without_change_axis(image, rect, padding=2)
                        image_group = cv2.bitwise_or(image_group, image_rect)
                    # cv2.imwrite('image_group.jpg', image_group)

                    horizontal_group, free_group = detector.detect(image_group,
                                                                min_size = 5,
                                                                text_threshold = 0.7,
                                                                link_threshold = 0.4,
                                                                mag_ratio = 2.,
                                                                slope_ths = 0.3,
                                                                height_ths = 0.1,
                                                                width_ths = 0.3)
                    horizontal_group, free_group = horizontal_group[0], free_group[0]
                    horizontal_group = [horizontal_to_rect(box) for box in horizontal_group]
                    rect_from_horizontal.extend(horizontal_group)
                template = Mapping.map_box_with_positions(template, rect_from_horizontal.copy())
                template = Mapping.clean_dulicates_rect(template)
                #
                # clone1 = image.copy()
                # for rect in rect_from_horizontal:
                #     clone1 = ImageProcessing.draw(clone1, rect)
                # cv2.imwrite('clone1.jpg', clone1)
                # clone3 = image.copy()
                # for rect in horizontal_group:
                #     clone3 = ImageProcessing.draw(clone3, rect)
                # cv2.imwrite('clone3.jpg', clone3)
                # clone2 = image.copy()
                # for key, rects in template.items():
                #     if len(rects.shape) == 3:
                #         for rect in rects:
                #             clone2 = ImageProcessing.draw(clone2, rect)
                #     else:
                #         clone2 = ImageProcessing.draw(clone2, rects)
                # cv2.imwrite('clone2.jpg', clone2)
                #
                for key, rects in template.items():
                    predict_list = []
                    if len(rects.shape) == 3:
                        for rect in rects:
                            predict_image = ImageProcessing.crop_with_padding(image, rect, padding=2)
                            predict_image = Image.fromarray(predict_image)
                            predict_list.append(predict_image)
                        lst_text = predictor.predict_batch(predict_list)
                        res = " ".join(lst_text)
                        res = NormalizeText.format_output(key, res)
                        template[key] = res
                    else:
                        predict_list = []
                        predict_image = ImageProcessing.crop_with_padding(image, rects, padding=2)
                        predict_image = Image.fromarray(predict_image)
                        res = predictor.predict(predict_image)
                        res = NormalizeText.format_output(key, res)
                        template[key] = res
                return template
            return {}
        except:
            return {}