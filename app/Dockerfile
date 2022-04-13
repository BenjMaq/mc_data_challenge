FROM python:latest
WORKDIR /tracker

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY tracker /tracker
CMD ["python", "-u", "app.py"]