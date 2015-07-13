FROM lbracken/flask-uwsgi
MAINTAINER Jacob Payne <paynejacob21@gmail.com>

RUN apt-get update
RUN apt-get install libavbin-dev libavbin0 postgresql-client -y

EXPOSE 5000

CMD ["uwsgi", "--socket :5000 --env APP_ENV=dev --wsgi-file wsgi.py --callable app --processes 2 --threads 4"]
