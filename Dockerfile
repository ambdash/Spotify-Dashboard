FROM python:3.9

ADD application/app.py .

COPY ./requirements.txt /root/requirements.txt

RUN  pip install -r /root/requirements.txt

WORKDIR /root/docker_test

COPY . /root/docker_test

CMD ["python", "./app.py"]