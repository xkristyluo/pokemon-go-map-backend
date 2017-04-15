FROM ubuntu:14.04
MAINTAINER Xi Luo <x.nancy.luo@gmail.com>

# Level 1
RUN apt-get update -y && apt-get install -y libpq-dev \
                                            python-dev \
                                            ssh

RUN apt-get install -y python-setuptools

RUN easy_install pip

ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Copy source code
ADD . /src

# Create a directory for log file crawler.log 
RUN mkdir -p /var/log/django

EXPOSE 8000

# run
CMD ["/src/start.sh"]

