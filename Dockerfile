FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 
COPY . /App
WORKDIR /App

RUN pip install -r requirements.txt
RUN pip3 install pycairo
RUN pip3 install PyGObject
ENTRYPOINT ["python3"]
CMD ["run.py"]