FROM ubuntu:14.04
MAINTAINER Xi Luo <x.nancy.luo@gmail.com>

# Level 1
RUN apt-get update -y && apt-get install -y libpq-dev \
                                            python-dev \
                                            ssh

RUN apt-get install -y python-setuptools

RUN easy_install pip

RUN pip install packaging

#RUN python -m pip install -U pip
#RUN pip install setuptools==33.1.1

ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Copy source code
ADD . /src

RUN mkdir -p /var/log/django

EXPOSE 8000

# run
CMD ["/src/start.sh"]
