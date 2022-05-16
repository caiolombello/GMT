ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION}

WORKDIR /app/
COPY *.py /app/

RUN echo "SSH Config" \
ssh-keygen -t rsa \
echo "As administrator, apply the following key to new Gitlab environment" \
cat rsa.pub \
echo "Press any key to continue" \
while [ true ] ; do \
read -t 3 -n 1 \
if [ $? = 0 ] ; then \
exit ; \
mkdir ~/.ssh && echo 'StrictHostKeyChecking=accept-new' > ~/.ssh/config

RUN pip3 install colorama requests urllib3 chardet
RUN python3 get-all.py && python3 post-all.py && python3 transfer-users.py
