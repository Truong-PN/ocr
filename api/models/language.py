from django.db import models


class LanguageModel(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_code = models.CharField(max_length=5,
                                        unique=True,
                                        verbose_name='Language code')
    name = models.CharField(max_length=30, unique=True, verbose_name='Name')

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(null=True, auto_now=True, editable=False)
