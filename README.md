# Document
I. Installing PostgreSQL
```
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service
```

II. Setup environment (python 3.8.8) \

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Note
* If the server has NVIDIA cuda, please install [packages cuda](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html) and [pytorch cuda](https://pytorch.org/)
* The version NVIDIA must be mapped with pytorch

III. Initial data
* Create database with user and password like is [settings](core/settings.py#L89)
* Run below command
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py initial
```

IV. Run service
```
nohup python3 manage.py runserver 0.0.0.0:8000 --noreload > nohup.log &
```

V. Configuration
* CORS: [settings](core/settings.py#L30)


VI. Postman
* Please import collection from [v1.postman_collection.json](v1.postman_collection.json) to postman
* Each test case, you can select image in [template](template) with format [template_id]_*.jpg
* Example:
```
template_id: 1
image:      [1]_cavet_xe_may_mat_truoc(cu).jpg
```

VII. Other command \
[Django command](https://docs.djangoproject.com/en/4.1/ref/django-admin)
