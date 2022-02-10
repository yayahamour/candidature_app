FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /App
WORKDIR /App
RUN apt-get update -y
RUN apt-get install -y pkg-config
RUN apt-get install libcairo2-dev libjpeg-dev libgif-dev
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["run.py"]