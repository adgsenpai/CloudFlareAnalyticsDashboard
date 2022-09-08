FROM ubuntu:20.04

LABEL Maintainer="adgsenpai"

EXPOSE 8000

RUN apt-get update

COPY . . 

RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

RUN pip3 install -r requirements.txt

CMD ["gunicorn","app:app","--timeout","99999"]
