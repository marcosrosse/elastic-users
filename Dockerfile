FROM python:alpine3.16

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD . .

RUN chmod -Rv 775 *

USER 1000

ENTRYPOINT ["python", "./main.py"]
