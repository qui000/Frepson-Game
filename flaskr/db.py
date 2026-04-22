import sqlite3
from datetime import datetime

import click
from flask import current_app, g
from flaskr.locale import giveLocations
from flaskr.items import giveItems


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def createLocations():

    for q in giveLocations():
        db = get_db()
        db.execute(
            'INSERT INTO location (full_name, posX, posY) VALUES (?, ?, ?)',
            (q.full_name, q.posX, q.posY),

        )
        db.commit()
    return

def createItems():

    for q in giveItems():
        db = get_db()
        db.execute(
            'INSERT INTO item (full_name, health, action, ownerID) VALUES (?, ?, ?, ?)',
            (q.full_name, q.health, q.action, q.ownerID),

        )
        db.commit()
    return

    


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()

    startTurn = 1
    db = get_db()
    db.execute(
        'INSERT INTO gamestate (turn) VALUES (?)',
        (startTurn,),

    )
    db.commit()

    createLocations()
    createItems()

    

    


    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)