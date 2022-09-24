FROM python:3.10-slim

COPY ./app /app
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./requirements.txt /requirements.txt
COPY /.env /.env
# COPY env only in testing


RUN apt-get update && \
    apt-get install -y  \
        build-essential \
        python3-dev \
        python3-setuptools \
        tesseract-ocr \
        make \
        gcc \
    && python3 -m pip install -r requirements.txt \
    && apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x /app/entrypoint.sh

CMD ["./app/entrypoint.sh"]