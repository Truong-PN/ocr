from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.models.template import TemplateModel
from base.enums.mode_detection import ModeDetection


class GetTemplateSerializer(serializers.Serializer):
    template_id = serializers.IntegerField(required=False)
    language_code = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

class CreateTemplateSerializer(serializers.ModelSerializer):
    language_code = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    template = serializers.DictField(required=False)
    box = serializers.DictField(required=False)
    mode = serializers.ChoiceField(choices=ModeDetection.choices,
                                    required=False)

    class Meta:
        model = TemplateModel
        fields = ('language_code', 'name', 'template', 'box', 'mode')

    def validate(self, attrs):
        template = attrs.get('template')
        box = attrs.get('box')

        if not template and not box:
            raise serializers.ValidationError({
                        "field": _(f'require at least field template/ box')
                    })

        if template and isinstance(template, dict):
            for key, values in template.items():
                if not isinstance(values, list):
                    raise serializers.ValidationError({
                        "template": _(f'field {key} must be list string')
                    })
                for value in values:
                    if not isinstance(value, str):
                        raise serializers.ValidationError({
                            "template": _(f'field {key} must be list string')
                        })
        if box and isinstance(box, dict):
            for key, values in box.items():
                if not isinstance(values, list):
                    raise serializers.ValidationError({
                        "box": _(f'field {key} must be list float')
                    })
                for value in values:
                    if not isinstance(value, float):
                        raise serializers.ValidationError({
                            "box": _(f'field {key} must be list float')
                        })
        return super().validate(attrs)

class UpdateTemplateSerializer(serializers.ModelSerializer):
    template_id = serializers.IntegerField(required=True)
    lanuage_code = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    template = serializers.DictField(required=False)
    box = serializers.DictField(required=False)
    mode = serializers.ChoiceField(choices=ModeDetection.choices,
                                    default= ModeDetection.TEXT_DETECTION,
                                    required=False)

    class Meta:
        model = TemplateModel
        fields = ('template_id', 'lanuage_code', 'name', 'template', 'box', 'mode')


    def validate(self, attrs):
        template = attrs.get('template')
        box = attrs.get('box')

        if not template and not box:
            raise serializers.ValidationError({
                        "field": _(f'require at least field template/ box')
                    })

        if template and isinstance(template, dict):
            for key, values in template.items():
                if not isinstance(values, list):
                    raise serializers.ValidationError({
                        "template": _(f'field {key} must be list string')
                    })
                for value in values:
                    if not isinstance(value, str):
                        raise serializers.ValidationError({
                            "template": _(f'field {key} must be list string')
                        })
        if box and isinstance(box, dict):
            for key, values in box.items():
                if not isinstance(values, list):
                    raise serializers.ValidationError({
                        "box": _(f'field {key} must be list float')
                    })
                for value in values:
                    if not isinstance(value, float):
                        raise serializers.ValidationError({
                            "box": _(f'field {key} must be list float')
                        })
        return super().validate(attrs)

class DeleteTemplateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = TemplateModel
        fields = ('id',)
