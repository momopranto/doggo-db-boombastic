FROM python:2.7

WORKDIR /opt/
ADD ./ /opt/
RUN DEBIAN_FRONTEND=noninteractive apt-get update && make setup

CMD make run
