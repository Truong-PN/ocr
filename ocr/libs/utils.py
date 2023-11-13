from functools import lru_cache

import tensorflow as tf

from api.models.language import LanguageModel


@lru_cache
def get_languages() -> list:
    data = LanguageModel.objects.all()
    language_code = list(data.values('language_code'))
    languages = [object.get('language_code') for object in language_code]
    return languages


@lru_cache
def get_device() -> bool:
    return True if tf.config.list_physical_devices('GPU') else False

def horizontal_to_rect(horizontal: list) -> list:
    l,r,t,b = horizontal
    tr = [r,t]
    br = [r,b]
    bl = [l,b]
    tl = [l,t]
    rect = [tr, br, bl, tl]
    return rect

def perspective_transform(horizontal_list: list):
    l,r,t,b = zip(*horizontal_list)
    shift_x = min(l)
    shift_y = min(t)
    crop_size_h = max(b)-shift_y
    crop_size_w = max(r)-shift_x
    return shift_x, shift_y, crop_size_h, crop_size_w