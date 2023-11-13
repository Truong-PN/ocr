from django.db import models
from dataclasses import dataclass, fields
from django.utils.translation import gettext_lazy as _

@dataclass
class ModeDetection(models.IntegerChoices):
    TEXT_DETECTION: int = 0, 'Text_detection'
    BOX_DETECTION: int = 1, 'Box_detection'

    @classmethod
    def get_all(cls):
        return [getattr(cls, f.name) for f in fields(cls)]