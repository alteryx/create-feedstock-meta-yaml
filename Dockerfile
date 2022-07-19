FROM python:3.8
ADD create_feedstock_meta_yaml create_feedstock_meta_yaml
ADD requirements.txt requirements.txt

RUN pip install pip --upgrade --progress-bar off
RUN pip install -r requirements.txt --progress-bar off
RUN python -c "import requests"
RUN python -c "import conda_forge_tick"
ENTRYPOINT ["python", "create_feedstock_meta_yaml/main.py"]
