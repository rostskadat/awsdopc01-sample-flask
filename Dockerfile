FROM ubuntu:latest

RUN set -ex \
	&& apt-get update \
	&& apt-get install -y \
 			python3-pip \
 			python3-dev \
 			build-essential \
 	&& apt-get clean \
 	&& rm -rf /var/lib/apt/lists/*

ENV APPPATH /app

COPY src/requirements.txt $APPPATH/requirements.txt
RUN pip3 --disable-pip-version-check install -r $APPPATH/requirements.txt
COPY src $APPPATH
WORKDIR $APPPATH
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
