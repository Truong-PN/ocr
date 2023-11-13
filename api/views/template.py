from rest_framework.decorators import action
from rest_framework.request import Request

from api.models.template import TemplateModel
from api.request.template import *
from base.response import FailedError, Response
from base.views import BaseViewSet
from api.response.template import TemplateResponse


class TemplateViewSet(BaseViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    queryset = TemplateModel.objects.all()

    # permission_classes = [permissions.AllowAny]
    serializer_classes = {
        "list": GetTemplateSerializer,
        "create": CreateTemplateSerializer,
        "update": UpdateTemplateSerializer,
        "destroy": DeleteTemplateSerializer,
    }

    def list(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        try:
            kwargs: dict = serializer.data
            records = TemplateModel.objects.filter(**kwargs)
            records_data = list(records.values())
            response = TemplateResponse(data=records_data)
        except:
            return Response()
        return Response(response)

    def create(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            kwargs: dict = serializer.data
            record = TemplateModel(**kwargs)
            record.save()
        except:
            return FailedError(message = "regist failed")
        return Response({ "status": "success", "message": "Successful!" })

    def update(self, request: Request, pk: int) -> Response:
        serializer = self.get_serializer(data={"id": pk, **request.data})
        serializer.is_valid(raise_exception=True)
        try:
            kwargs: dict = serializer.data
            TemplateModel.objects.filter(id=pk).update(**kwargs)
        except:
            pass
        return Response({ "status": "success", "message": "Successful!" })

    def destroy(self, _: Request, pk: int) -> Response:
        serializer = self.get_serializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)
        try:
            TemplateModel.objects.filter(id=pk).delete()
        except:
            pass
        return Response({ "status": "success", "message": "Successful!" })
