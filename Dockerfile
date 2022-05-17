ARG PYTHON_VERSION=3.8.10

FROM python:${PYTHON_VERSION}

ARG RSA
ARG OLD_ORIGIN_API
ARG OLD_ORIGIN_TOKEN
ARG ORIGIN_IP
ARG ORIGIN_API
ARG ORIGIN_TOKEN

COPY ${RSA} ./${RSA}
COPY ${RSA}.pub ./${RSA}.pub
RUN mkdir ~/.ssh
COPY config root/.ssh/config

RUN echo '\nPlease, enter the following RSA public key at http://yourhost:8080/-/profile/keys to proceed:' && \
cat ${RSA}.pub

RUN echo "${ORIGIN_IP}  localhost" > /etc/hosts && \
echo 'StrictHostKeyChecking=no' > /etc/ssh/ssh_config

WORKDIR /app/
COPY *.py /app/ 

RUN python3 -m pip install --upgrade pip && \
pip3 install colorama requests urllib3 chardet

# RUN python3 get-all.py && \
# python3 post-all.py
