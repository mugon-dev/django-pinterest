FROM python:3.9.0

WORKDIR /home/

RUN echo "testing"

RUN git clone https://github.com/mugon-dev/django-pinterest.git

WORKDIR /home/django-pinterest/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

RUN python manage.py collectstatic

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate --settings=config.settings.deploy && gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.deploy config.wsgi --bind 0.0.0.0:8000"]