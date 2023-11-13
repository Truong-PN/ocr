import os
import re

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.middleware.csrf import _get_new_csrf_string as generate_csrf_token

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from base.serializers import BaseSerializer


class BaseViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    serializer_class = BaseSerializer
    permission_classes = [permissions.AllowAny]

    serializer_classes = {}

    def get_serializer(self, *args, **kwargs):
        self.serializer_class = self.serializer_classes.get(self.action, BaseSerializer)
        return super().get_serializer(*args, **kwargs)
