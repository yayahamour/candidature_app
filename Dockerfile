FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN sudo apt install libgirepository1.0-dev
COPY . /App
WORKDIR /App
RUN pip install -r requirements.txt
RUN pip3 install pycairo
RUN pip3 install PyGObject

ENTRYPOINT ["python2"]
CMD ["run.py"]