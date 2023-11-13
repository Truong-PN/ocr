from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.models.template import TemplateModel


class OcrSerializer(serializers.Serializer):
    template_id = serializers.IntegerField(required=True)
    image = serializers.ImageField(required=True)

    def validate(self, attrs):
        template_id = attrs.get('template_id')
        if template_id and isinstance(template_id, int):
            check_exists = TemplateModel.objects.filter(template_id=template_id)
            if not check_exists:
                raise serializers.ValidationError({
                        "template_id" : _(f'{template_id} is not exists')
                    })
        return super().validate(attrs)
