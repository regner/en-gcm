

FROM debian:latest

RUN apt-get update -qq \
&& apt-get upgrade -y \
&& apt-get install -y python-dev python-pip \
&& apt-get autoremove -y \
&& apt-get clean autoclean

RUN pip install -U pip

ADD en_gcm.py /en_gcm/
ADD requirements.txt /en_gcm/
ADD docker-entrypoint.sh /docker-entrypoint.sh

WORKDIR /en_gcm

RUN pip install -r requirements.txt 

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD gunicorn en_gcm:app -w 1 -b 0.0.0.0:8000 --log-level info --timeout 120 --pid /en_gcm/en_gcm.pid
