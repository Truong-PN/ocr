import json
from typing import List

from pydantic import BaseModel

from base.response import Data


class TemplateData(BaseModel):
    template_id: int
    language_code: str
    name: str
    template: dict
    box: dict
    mode: int
    is_master: bool

    class Config:
        fields = {
            'language_code': 'language_code_id'
        }

    def __init__(self, **attrs):
        template:str = attrs["template"]
        box:str = attrs["box"]
        attrs["template"] = json.loads(template.replace('\'','\"'))
        attrs["box"] = json.loads(box.replace('\'','\"'))
        super().__init__(**attrs)

class TemplateResponse(Data):
    data: List[TemplateData]
