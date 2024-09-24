FROM python:3.11

WORKDIR /code

RUN apt update
RUN apt install -y cron
COPY ml-work-cronjob /etc/cron.d/ml-work-cronjob
RUN crontab /etc/cron.d/ml-work-cronjob

COPY src/mnist/main.py /code/
COPY run.sh /code/run.sh
COPY note/mnist240924.keras /code

RUN pip install --no-cache-dir --upgrade git+https://github.com/HaramSs/mnist.git@0.7.0

CMD ["sh", "run.sh"]
