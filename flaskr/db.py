import sqlite3
from datetime import datetime

import click
from flask import current_app, g
from flaskr.locale import giveLocations
from flaskr.items import giveItems
from flaskr.npcs import startingNPCs
from flaskr.structures import starting_structures

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
            'INSERT INTO location (full_name, posX, posY, action, type, status) VALUES (?, ?, ?, ?, ?, ?)',
            (q.full_name, q.posX, q.posY, q.action, q.type, q.status),

        )
        db.commit()
    return

def createItems():

    for q in giveItems():
        db = get_db()
        db.execute(
            'INSERT INTO item (full_name, health, action, ownerID, armorType) VALUES (?, ?, ?, ?, ?)',
            (q.full_name, q.health, q.action, q.ownerID, q.armorType),

        )
        db.commit()
    return

def createStartingNPCs():

    for q in startingNPCs:
        db = get_db()
        db.execute(
            "INSERT INTO user (username, password, health, max_health, room, kind, action_points, max_action_points, visible, alive, canAct, mood, posX, posY) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (q.username, "123", q.health, q.max_health, q.room, q.kind, q.action_points, q.max_action_points, q.visible, q.alive, q.canAct, q.mood, q.posX, q.posY),
        )
        db.commit()
    return

def createStartingStructures():

    for q in starting_structures:
        db = get_db()
        db.execute(
            "INSERT INTO structure (full_name, action, type, ownerID, level, posX, posY, health, max_health) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (q.full_name, q.action, q.type, q.ownerID, q.level, q.posX, q.posY, q.health, q.max_health),
        )
        db.commit()
    return

def highestID_ALL():

    
    highestID = get_db().execute(
            'SELECT MAX(id) AS id FROM user',
                
            ).fetchone()
    
    if highestID != None:
        return int(highestID['id'])
    return 9999


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()


    createLocations()
    createItems()
    createStartingNPCs()
    createStartingStructures()

    
    
    startTurn = (highestID_ALL() + 1)
    db = get_db()
    db.execute(
        'INSERT INTO gamestate (turn) VALUES (?)',
        (startTurn,),

    )
    db.commit()
    
    
    


    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)