FROM python:3.9.0

WORKDIR /home/

RUN git clone https://github.com/mugon-dev/django-pinterest.git

WORKDIR /home/django-pinterest/

RUN pip install -r requirements.txt

RUN echo "SECRET_KEY=django-insecure-s*vtxd!$m-@2(#_8)1x4pi904g&%+fsh6o=phs1=&a$-$36w_d" > .env

RUN python manage.py migrate

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]