## -*- dockerfile-image-name: "ghcr.io/jh-ospo/fossfund-flask" -*-

FROM python:3.9.2-buster

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install uwsgi && \
    mkdir /working 

COPY app/ /working/app
COPY migrations/ working/migrations
COPY uwsgi* /working/
WORKDIR /working
CMD ["uwsgi", "--ini", "uwsgi.ini" ]

