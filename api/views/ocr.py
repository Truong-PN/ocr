import logging
import os

from django.conf import settings
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.request import Request

from api.models.ocr import OcrModel
from api.models.template import TemplateModel
from api.request.ocr import OcrSerializer
from api.response.ocr import OCRResponse
from base.response import Response
from base.views import BaseViewSet
from ocr.v1.process import ProcessOCRV1
from ocr.v2.process import ProcessOCRV2

logger = logging.getLogger(__name__)

class OCRViewSet(BaseViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # permission_classes = [permissions.AllowAny]
    serializer_classes = {
        'ocrv1': OcrSerializer,
        'ocrv2': OcrSerializer
    }

    @action(methods=['POST', ], detail=False, url_path='v1')
    def ocrv1(self, request: Request) -> Response:
        template_id = request.data.get('template_id', '')
        logger.info(f'template_id: {template_id}')
        if request.data.get('image', '') != '':
            file_name = request.data.get('image').name
            logger.info(f'image: {file_name}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template_id = serializer.data.get('template_id')
        image = request.FILES.get('image')
        path = os.path.normpath(os.path.join(settings.IMAGE_PATH, image.name))
        kwargs: dict = {
            'template_id': TemplateModel(template_id=template_id),
            'image_upload': path
        }
        new_record = OcrModel(**kwargs)
        new_record.image_upload.save(path, image)
        image_path = new_record.image_upload.path
        running = ProcessOCRV1.get_instance()
        template_data = running(template_id=template_id, image_upload=image_path)
        response = OCRResponse(data=template_data)
        return Response(response)


    @action(methods=['POST', ], detail=False, url_path='v2')
    def ocrv2(self, request: Request) -> Response:
        template_id = request.data.get('template_id', '')
        logger.info(f'template_id: {template_id}')
        if request.data.get('image', '') != '':
            file_name = request.data.get('image').name
            logger.info(f'image: {file_name}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template_id = serializer.data.get('template_id')
        image = request.FILES.get('image')
        path = os.path.normpath(os.path.join(settings.IMAGE_PATH, image.name))
        kwargs: dict = {
            'template_id': TemplateModel(template_id=template_id),
            'image_upload': path
        }
        new_record = OcrModel(**kwargs)
        new_record.image_upload.save(path, image)
        image_path = new_record.image_upload.path
        running = ProcessOCRV2.get_instance()
        template_data = running(template_id=template_id, image_upload=image_path)
        response = OCRResponse(data=template_data)
        return Response(response)