FROM alpine:latest

RUN apk --update --no-cache add \
      ca-certificates \
      freetype-dev \
      g++ \
      gcc \
      lvm2 \
      pkgconfig \
      python \
      python-dev \
      py2-pip \
      openssl && \
    rm -vf /var/cache/apk/* && \
    update-ca-certificates

RUN pip install --no-cache-dir --upgrade pip && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

COPY volcreate.py /srv/volcreate.py
COPY tgt.conf.j2 /srv/tgt.conf.j2

ENTRYPOINT ["/srv/volcreate.py"]
