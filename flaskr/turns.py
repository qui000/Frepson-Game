from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db
import click


def giveActionPoints(username, number):

    db = get_db()

    db.execute(
        'UPDATE user SET action_points = action_points + ? WHERE username = ?',
        (number, username)
    )
    db.commit()

    return

def checkTurn():

    
    gamestate = get_db().execute(
            'SELECT * FROM gamestate'
        ).fetchone()
        
    return int(gamestate['turn'])

def highestID():

    
    highestID = get_db().execute(
            'SELECT MAX(id) AS id FROM user WHERE canAct = 1',
                
            ).fetchone()
    
    
    return int(highestID['id'])

def lowestID():

    
    lowestID = get_db().execute(
            'SELECT MIN(id) AS id FROM user WHERE canAct = 1',
                
            ).fetchone()
    
    return int(lowestID['id'])

def nextID():

    
    largerIDs = get_db().execute(
            'SELECT id AS id FROM user WHERE id > ? AND canAct = 1 ORDER BY id ASC', (checkTurn(),)
                
            ).fetchall()
    
    if int(largerIDs[0]['id']):
        return int(largerIDs[0]['id'])

def changeTurn():

    

    if checkTurn() == highestID():
        db = get_db()

        db.execute(
            'UPDATE gamestate SET turn = ?', (lowestID(), )
            
        )
        db.commit()

        db = get_db()

        db.execute(
            'UPDATE gamestate SET gameloops = gameloops + 1', 
            
        )
        db.commit()
        return
    
    db = get_db()

    db.execute(
        'UPDATE gamestate SET turn = ?', (nextID(), )
        
    )
    db.commit()
    click.echo("changed turn")

    return

def currentTurnUser():

    theItem = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (checkTurn(),)
        ).fetchone()
    click.echo("checked turn")
    
    return theItem







