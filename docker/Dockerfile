FROM tiangolo/uwsgi-nginx:python2.7

RUN apk add postgresql-client postgresql git build-base gcc cmake autoconf automake libtool
RUN mv /app/uwsgi.ini /
RUN rm -rf /app/*
RUN mv /uwsgi.ini /app/

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/bin/supervisord"]
