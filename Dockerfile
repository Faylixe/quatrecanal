FROM debian:jessie
MAINTAINER Faylixe "felix.voituret@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY quatrecanal.py .

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["quatrecanal.py"]
