from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.ocr import OCRViewSet
from api.views.template import TemplateViewSet
from api.views.language import LanguageViewSet

router = DefaultRouter(trailing_slash=False)
router.register('ocr', OCRViewSet, basename='ocr')
router.register('template', TemplateViewSet, basename='template')
router.register('language', LanguageViewSet, basename='language')

urlpatterns = [
    path('', include(router.urls))
]
