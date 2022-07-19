FROM continuumio/miniconda3:4.12.0

SHELL ["/bin/bash", "--login", "-c"]
RUN git clone --depth 1 https://github.com/regro/cf-scripts.git

COPY environment.yml .
RUN conda env create -f environment.yml
RUN conda install -c conda-forge --file cf-scripts/requirements/run

SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

RUN python -c "import requests"
RUN cd cf-scripts && python setup.py install
RUN python -c "import conda_forge_tick"

ADD create_feedstock_meta_yaml create_feedstock_meta_yaml
ENTRYPOINT ["python", "/create_feedstock_meta_yaml/main.py"]
