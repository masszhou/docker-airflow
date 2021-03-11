# build: 
#   docker build --rm -t masszhou/docker-airflow:1.10.9-passat -f passat.Dockerfile .
# inspection: 
#   docker exec -ti docker-airflow_webserver_1 bash

FROM masszhou/docker-airflow:1.10.9-gcp
LABEL maintainer="Zhiliang Zhou <zhouzhiliang@gmail.com>"

# Airflow
ARG AIRFLOW_VERSION=1.10.9
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install \
    ffmpeg \
    libsm6 \
    libxext6 \
    && pip install rosbag tdqm pymongo opencv-python pandas numpy \
    && pip install google-cloud-storage httplib2 google-cloud google-api-python-client google-auth-httplib2 \
    && pip install pandas xlrd olefile pyarrow aiohttp alpha_vantage

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]