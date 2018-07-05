FROM python:3.6

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app/

ENTRYPOINT ["/usr/local/bin/python", "power-reporter.py"]
