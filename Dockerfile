FROM ubuntu:latest

RUN mkdir /app

# Python.
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && cd /

# Supervisor.
RUN echo exit 0 > /usr/sbin/policy-rc.d
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY /build/conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /app
COPY settings.py /app/settings.py
COPY main.py /app/main.py

ENTRYPOINT ["/usr/bin/supervisord"]