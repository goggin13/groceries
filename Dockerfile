FROM python:3.9.0-slim

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common
RUN apt-get install -y gcc

RUN pip install --upgrade pip
RUN pip install flask
RUN pip install pytest
RUN pip install psycopg2

ENV APP_ROOT /var/www/grocery-list
ENV FLASK_ENV=development
ENV FLASK_APP=groceries
ENV SECRET_KEY=development-secret-key

# Run the rest of the commands as the ``postgres`` user created by the ``postgres-9.3`` package when it was ``apt-get installed``
USER postgres

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `docker` owned by the ``docker`` role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker docker

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/11/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/11/main/postgresql.conf

# psql -h localhost -p 5432 -d docker -U docker --password

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

USER root

WORKDIR $APP_ROOT
COPY . .
RUN pip install -e .
CMD service postgresql start && python -m flask run --host=0.0.0.0
