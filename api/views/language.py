from rest_framework.decorators import action
from rest_framework.request import Request

from api.models.language import LanguageModel
from base.response import FailedError, Response
from base.views import BaseViewSet
from api.response.language import LanuageResponse
from api.request.language import *

class LanguageViewSet(BaseViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    queryset = LanguageModel.objects.all()
    serializer_classes = {
        'list': GetLanguageSerializer
    }

    def list(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        try:
            kwargs: dict = serializer.data
            records = LanguageModel.objects.filter(**kwargs)
            records_data = list(records.values())
            response = LanuageResponse(data=records_data)
        except:
            return FailedError(message = "Dictionary already exists")
        return Response(response)
