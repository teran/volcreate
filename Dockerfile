FROM ubuntu:xenial

RUN apt-get update && \
    apt-get install -y \
      lvm2 \
      python \
      python-dev \
      python-pip \
      python-pkgconfig \
      tgt && \
    apt-get clean && \
    rm -rvf /var/lib/apt/lists/*


RUN pip install --no-cache-dir --upgrade pip && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

COPY volcreate.py /srv/volcreate.py
COPY tgt.conf.j2 /srv/tgt.conf.j2

ENTRYPOINT ["/srv/volcreate.py"]
