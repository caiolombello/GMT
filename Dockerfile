ARG PYTHON_VERSION=3.8.10

FROM python:${PYTHON_VERSION}

ARG RSA
ARG OLD_ORIGIN_API
ARG OLD_ORIGIN_TOKEN
ARG ORIGIN_API
ARG ORIGIN_TOKEN

RUN echo 'StrictHostKeyChecking=accept-new' > /etc/ssh/ssh_config

WORKDIR /app/
COPY *.py /app/

RUN apt-get install git

RUN python3 -m pip install --upgrade pip && \
pip3 install colorama requests urllib3 chardet && \
python3 get-all.py && \
python3 post-all.py && \
python3 transfer-users.py
