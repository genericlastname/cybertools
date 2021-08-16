import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app):
    '''Set up app database functions.'''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    '''Load the database schema.'''
    db = get_db()

    with current_app.open_resource('db/schema.sql') as f:
        script = f.read()
        db.executescript(script.decode())

@click.command('init-db')
@with_appcontext
def init_db_command():
    '''Clear data and create tables.'''
    init_db()
    click.echo('Database initialized.')

def get_db():
    '''Connect to sql database.'''
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    '''Close the open database in the request.'''
    db = g.pop('db', None)

    if db is not None:
        db.close()
