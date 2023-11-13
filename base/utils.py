import os
import sys
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler
from urllib.request import urlretrieve
from zipfile import ZipFile

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if isinstance(exc, NotAuthenticated):
        return Response({"status": "unauthorized", "message": "Token is invalid or expired"}, status=status.HTTP_401_UNAUTHORIZED)
    # Now add the HTTP status code to the response.
    if response is not None:
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response({"status": "unauthorized", "message": "Token is invalid or expired"}, status=status.HTTP_401_UNAUTHORIZED)
    # default case
    return exception_handler(exc, context)

def printProgressBar(prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    def progress_hook(count, blockSize, totalSize):
        progress = count * blockSize / totalSize
        percent = ("{0:." + str(decimals) + "f}").format(progress * 100)
        filledLength = int(length * progress)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')

    return progress_hook

def download_and_unzip(url, filename, path):
    zip_path = os.path.join(path, 'temp.zip')
    reporthook = printProgressBar(prefix='Progress:', suffix='Complete', length=50)
    urlretrieve(url, zip_path, reporthook=reporthook)
    with ZipFile(zip_path, 'r') as zipObj:
        zipObj.extract(filename, path)
    os.remove(zip_path)
    print()

def load_env():
    for key, value in settings.ENVIRONMENT.items():
        os.environ[key] = value

    for path in settings.SYSPATH:
        sys.path.append(path)
