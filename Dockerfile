ARG PYTHON_VERSION=3.8.10

FROM python:${PYTHON_VERSION}

ARG RSA
ARG SOURCE_ID
ARG OLD_ORIGIN_API
ARG OLD_ORIGIN_TOKEN
ARG ORIGIN_IP
ARG ORIGIN_API
ARG ORIGIN_TOKEN

ENV RSA=${RSA}
ENV SOURCE_ID=${SOURCE_ID}
ENV OLD_ORIGIN_API=${OLD_ORIGIN_API}
ENV OLD_ORIGIN_TOKEN=${OLD_ORIGIN_TOKEN}
ENV ORIGIN_IP=${ORIGIN_IP}
ENV ORIGIN_API=${ORIGIN_API}
ENV ORIGIN_TOKEN=${ORIGIN_TOKEN}

ENTRYPOINT ["/bin/sh", "-c" , "mkdir ~/.ssh || echo ${ORIGIN_IP}  localhost > /etc/hosts && echo 'StrictHostKeyChecking=no' > /etc/ssh/ssh_config && bash" ]

COPY ${RSA} ./${RSA}
COPY ${RSA}.pub ./${RSA}.pub
COPY config root/.ssh/config

WORKDIR /app/
COPY *.py /app/ 

RUN python3 -m pip install --upgrade pip && \
pip3 install colorama requests urllib3 chardet

