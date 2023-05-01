FROM python:3.7-alpine
COPY requirements.txt ipv64_client.py functions.py /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV NodeSecret=empty
RUN if [ "$NodeSecret" == "empty" ]; then echo "NEED NodeSecret"; exit 1; fi
CMD ["python", "ipv64_client.py", "$NodeSecret"]
