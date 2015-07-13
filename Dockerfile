FROM python:2.7
MAINTAINER Jacob Payne <paynejacob21@gmail.com>

ADD . /app
WORKDIR /app
RUN apt-get update && apt-get install -y \
  libpq-dev \
  python-dev

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "--socket :5000 --env APP_ENV=dev --wsgi-file wsgi.py --callable app --processes 2 --threads 4"]
