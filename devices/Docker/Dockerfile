FROM python:3.7-alpine
COPY ../../requirements.txt ../../ipv64_client.py ../../functions.py /app/
WORKDIR /app
RUN pip install -r requirements.txt
ENV NodeSecret=empty

CMD ["python","-u", "ipv64_client.py"]
