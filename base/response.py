from pydantic import BaseModel
from rest_framework import response, status


class Data(BaseModel):
    status: str = 'success'

class Response(response.Response):
    def __init__(self, data: BaseModel = [], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = status.HTTP_200_OK
        self.data = data.dict() if isinstance(data, BaseModel) else {"status":"success", "data": []}

class FailedError(response.Response):
    def __init__(self, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = status.HTTP_400_BAD_REQUEST
        self.data = {
            "status": "failed",
            "message": message
        }

class ForbiddenError(response.Response):
    def __init__(self, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = status.HTTP_403_FORBIDDEN
        self.data = {
            "status": "forbidden",
            "message": message
        }
