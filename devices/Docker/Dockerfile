FROM python:3.8-alpine

ENV Node64Secret=''
ENV Node64Color=False
ENV Node64Script='node64.py'

COPY --chmod=777 devices/Docker/entry.sh /entry.sh
COPY ./requirements.txt ./node64.py /app/
COPY ./Node64Client /app/Node64Client

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["/entry.sh"]


