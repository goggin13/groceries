FROM python:3.9.0-slim

RUN apt-get update
RUN apt-get install -y curl

RUN pip install --upgrade pip
RUN pip install flask
RUN pip install pytest

ENV APP_ROOT /var/www/grocery-list
ENV FLASK_ENV=development
ENV FLASK_APP=groceries
ENV SECRET_KEY=development-secret-key

WORKDIR $APP_ROOT
COPY . .
RUN pip install -e .
RUN python -m flask init-db
CMD python -m flask run --host=0.0.0.0 -p $PORT
