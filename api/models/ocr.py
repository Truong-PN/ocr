from django.db import models

from api.models.template import TemplateModel


class OcrModel(models.Model):
    id = models.AutoField(primary_key=True)
    template_id = models.ForeignKey(TemplateModel,
                                        to_field="template_id",
                                        on_delete=models.CASCADE)
    # preprocessing
    image_upload = models.ImageField(max_length=255,
                                        null=True,
                                        verbose_name='Image upload')
    image_ocr = models.ImageField(max_length=255,
                                        null=True,
                                        verbose_name='Image ocr')
    # mapping template
    content = models.JSONField(null=True, verbose_name='Content')
    data = models.JSONField(null=True, verbose_name='Data')
    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(null=True, auto_now=True, editable=False)