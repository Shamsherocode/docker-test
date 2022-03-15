FROM python:3.9-slim

# RUN apt-get update && apt-get install build-essential -y

ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip install --upgrade pip
# RUN apt-get update \
#     && apt-get -y install libpq-dev gcc
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./hututoo /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
