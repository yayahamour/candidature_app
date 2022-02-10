FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /App
WORKDIR /App
RUN pip install -r requirements.txt
RUN pip install PyGObject
ENTRYPOINT ["python3"]
CMD ["run.py"]