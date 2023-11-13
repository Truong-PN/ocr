from django.db import models

from api.models.language import LanguageModel
from base.enums.mode_detection import ModeDetection


class TemplateModel(models.Model):
    template_id = models.AutoField(primary_key=True)
    language_code = models.ForeignKey(LanguageModel,
                                        to_field="language_code",
                                        on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50, verbose_name='Name')
    template = models.TextField(null=True, verbose_name='Template')
    box = models.TextField(null=True, verbose_name='Box position')
    mode = models.IntegerField(choices=ModeDetection.choices,
                                default= ModeDetection.TEXT_DETECTION,
                                verbose_name='Mode detection')
    is_master = models.BooleanField(default=False, verbose_name='Is master')

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(null=True, auto_now=True, editable=False)
