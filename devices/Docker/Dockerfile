FROM python:3.8-alpine

COPY --chmod=777 entry.sh /entry.sh
COPY ../../requirements.txt ../../node64.py ../../Node64Client /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENV NodeSecret=''
ENV Node64Color=False
ENV Node64Script='node64.py'

ENTRYPOINT ["/entry.sh"]


