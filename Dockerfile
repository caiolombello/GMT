ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION}

WORKDIR /app/
COPY *.py /app/
RUN pip3 install colorama requests urllib3 chardet
RUN python3 get-all.py && python3 post-all.py && python3 transfer-users.py
