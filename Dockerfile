FROM python:3.7-alpine

LABEL MAINTAINER="XCNT GmbH <dev-infra@xcnt.io>"

WORKDIR /opt/app

ADD requirements.txt /opt/app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev linux-headers && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

ADD . /opt/app

USER 9000

CMD [ "python", "cname_record_setter.py" ]
