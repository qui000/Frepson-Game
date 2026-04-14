from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db
from flaskr.turns import giveActionPoints, changeTurn, checkTurn
import click

def giveAllActions():
    all_actions = ["move","punch"]

    return all_actions


def checkCurrentUser(for_what):

    user_detail = g.user[for_what]
    
    click.echo(user_detail)
    return user_detail

def checkForSame(for_what, username):

    user_detail = get_db().execute(
            'SELECT ? FROM user WHERE locale = ? AND username = ?', (for_what, g.user['locale'], username,)
            ).fetchone()
    
    
    return user_detail



def takeAction(full_name):

    message = None
    name = full_name.split()
    action = name[0]
    last_turn = False
    if len(name) > 1:
        object = name[1]

    if (int(checkCurrentUser('action_points')) < 1) or checkTurn() != int(g.user['id']):
        return 'It is not your turn.'
    if int(checkCurrentUser('action_points')) == 1:
        last_turn = True
        



    if action == "move":
        changeLocale(g.user['username'],1)
        giveActionPoints(g.user['username'],-1)
        message = "moved"

    
    if action == "punch":
        message = ("realized there is no person named "+object+" here to punch. He punches the air in vain")
        if checkForSame('username', object) != None:
            changeHealth(object, -1)
            giveActionPoints(g.user['username'],-1)
            message = ("punched "+object)
        
    if (message != None) and last_turn == True:
        changeTurn()
        
            
    return message
        
def changeHealth(who, amount):
    db = get_db()
    db.execute(
                'UPDATE user SET health = health + ? WHERE username = ?',
                (amount, who),
            )
    db.commit()

    return

def changeLocale(who,where):

    db = get_db()
    db.execute(
                'UPDATE user SET locale = locale + ? WHERE username = ?',
                (where, who),
            )
    db.commit()

    return