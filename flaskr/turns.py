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
    return int(g.gamestate['turn'])

def highestID():
    return int(g.highestID['id'])

def changeTurn():

    

    if checkTurn() == highestID():
        db = get_db()

        db.execute(
            'UPDATE gamestate SET turn = 1'
            
        )
        db.commit()
        return
    
    db = get_db()

    db.execute(
        'UPDATE gamestate SET turn = turn + 1'
        
    )
    db.commit()

    return







