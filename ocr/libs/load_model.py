from pathlib import Path

from django.conf import settings

from base.utils import download_and_unzip


class LoadModel:
    def __init__(self):
        self.config_model: dict = settings.MODEL
        self.model_root: Path = settings.MODEL_ROOT

    def download(self):
        Path(self.model_root).mkdir(parents=True, exist_ok=True)
        for key, model in self.config_model.items():
            url = model['url']
            filename = model['filename']
            if not Path(self.model_root / filename).is_file():
                print(f'Download {key}')
                download_and_unzip(url, filename, self.model_root)

    def info(self) -> list:
        return list(self.model_root.glob('*.*'))
