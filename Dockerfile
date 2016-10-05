FROM debian:jessie
MAINTAINER Faylixe "felix.voituret@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN pip install requests flask
COPY . quatrecanal.py
RUN pip install requests flask

ENTRYPOINT ["python"]
CMD ["quatrecanal.py"]
