FROM lbracken/flask-uwsgi
MAINTAINER Jacob Payne <paynejacob21@gmail.com>

EXPOSE 5000

CMD ["uwsgi", "--socket :5000 --env APP_ENV=dev --wsgi-file wsgi.py --callable app --processes 2 --threads 4"]
