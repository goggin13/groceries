import sqlite3
import click
import psycopg2
import urllib.parse as urlparse
import os
from flask import current_app, g
from flask.cli import with_appcontext

def get_heroku_db():
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

def get_local_db():
    dbname = "docker"
    user = "docker"
    password = "docker"
    host = "localhost"
    port = 5432

    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

def get_db():
    if 'connection' not in g:
        if 'DATABASE_URL' in os.environ:
            g.connection = get_heroku_db()
        else:
            g.connection = get_local_db()

    return g.connection

def close_db(e=None):
    db = g.pop('connection', None)

    if db is not None:
        db.close()

def init_db():
    connection = get_db()
    connection.cursor().execute(open("groceries/schema.sql", "r").read())
    connection.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def query(query):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()

    return result
