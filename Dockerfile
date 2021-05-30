FROM python:3.9.0

RUN mkdir /root/.ssh

# 만들어진 image를 다른 사람이 다운 받으면 그 사람도 ssh 키에 접근 가능
ADD ./.ssh/id_rsa /root/.ssh/id_rsa

RUN chmod 600 /root/.ssh/id_rsa

RUN touch /root/.ssh/known_hosts

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

WORKDIR /home/

RUN echo "testing1234"

RUN git clone https://github.com/mugon-dev/django-pinterest.git

# RUN git clone git@github.com:user/project.git

WORKDIR /home/django-pinterest/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=config.settings.deploy && python manage.py migrate --settings=config.settings.deploy && gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.deploy config.wsgi --bind 0.0.0.0:8000"]