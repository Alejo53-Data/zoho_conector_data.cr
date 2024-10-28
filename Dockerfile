FROM python:3.9.6-buster

RUN apt-get update && apt upgrade -y 

RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

WORKDIR /zcrm-connector

COPY . /zcrm-connector

RUN pip3 install -r requirements.txt

EXPOSE 5002

CMD ["flask", "run", "--host=0.0.0.0","--port=5002"]
