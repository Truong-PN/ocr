from rest_framework import serializers


class GetLanguageSerializer(serializers.Serializer):
    language_id = serializers.IntegerField(required=False)
    language_code = serializers.CharField(required=False)
    name = serializers.CharField(required=False)