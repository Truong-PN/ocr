from typing import Tuple
import numpy as np
from django.conf import settings
from shapely.geometry.polygon import Polygon


class Mapping:

    @staticmethod
    def map_box_with_positions(template_box: dict, rects: list)->dict:
        template_box = dict(reversed(list(template_box.items())))
        for key, box in template_box.items():
            polygon_key = Polygon(box)
            list_res = []
            clone_rects = rects.copy()
            for rect in clone_rects:
                polygon_rect = Polygon(rect)
                rect_area = polygon_rect.area
                check_area = polygon_rect.intersection(polygon_key).area
                if check_area / rect_area >= settings.THRESH_AREA:
                    list_res.append(rect)
                    rects.remove(rect)
            if list_res:
                template_box[key] = np.array(list_res)
        template_box = dict(reversed(list(template_box.items())))
        return template_box

    @staticmethod
    def clean_dulicates_rect(template_box: dict)->dict:
        for key, rects in template_box.items():
            clone: np.ndarray = rects.copy()
            clone: list = clone.tolist()
            rects = np.array(rects)
            shape = len(rects.shape)
            if shape == 3:
                for i in range(len(rects)-1):
                    for j in range(i+1, len(rects)):
                        polygon_i = Polygon(rects[i])
                        polygon_j = Polygon(rects[j])
                        area_i_j = polygon_i.intersection(polygon_j).area
                        if area_i_j / polygon_i.area >= settings.THRESH_DUPLICATE:
                            clone.remove(rects[i].tolist())
                            break
            template_box[key] = np.array(clone)
        return template_box

    @staticmethod
    def format_template(template_box: dict)-> Tuple[dict, list]:
        rect_group = []
        if "group" in template_box:
            rect_group: list = template_box["group"].copy()
            del template_box["group"]
        return template_box, rect_group
