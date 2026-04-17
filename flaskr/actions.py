from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db
from flaskr.turns import giveActionPoints, changeTurn, checkTurn
import click

gridSize = 2

def giveAllActions():
    all_actions = ["move","punch"]

    return all_actions


def checkCurrentUser(for_what):

    user_detail = g.user[for_what]
    
    
    return user_detail

def sameCurrentLocation(username):

    user_detail = get_db().execute(
            'SELECT id FROM user WHERE posX = ? AND posY = ? AND username = ?', (g.location['posX'], g.location['posY'], username,)
            ).fetchone()
    
    click.echo(user_detail)
    return user_detail



def takeAction(full_name):

    message = None
    name = full_name.split()
    action = name[0].lower()
    last_turn = False
    currentUsername = g.user['username']
    if len(name) > 1:
        object = name[1]

    if (int(checkCurrentUser('action_points')) < 1) or checkTurn() != int(g.user['id']):
        return 'It is not your turn.'
    if int(checkCurrentUser('action_points')) == 1:
        last_turn = True
        



    if action == "move":
        object = object.lower()
        if object == "north":
            
            
            message = "tried to wade into the black water, but didn't make it far."
            if checkLocaleMove(1,'posY') == True:
                changeLocale(1,'posY',currentUsername)
                giveActionPoints(currentUsername,-1)
                message = "went North"

        if object == "south":
            
            
            message = "tried to wade into the yellow water, but didn't make it far."
            if checkLocaleMove(-1,'posY') == True:
                changeLocale(-1,'posY',currentUsername)
                giveActionPoints(currentUsername,-1)
                message = "went South"
        
        if object == "east":
            
            
            message = "tried to wade into the pink water, but didn't make it far."
            if checkLocaleMove(1,'posX') == True:
                changeLocale(1,'posX',currentUsername)
                giveActionPoints(currentUsername,-1)
                message = "went East"

        if object == "west":
            
            
            message = "tried to wade into the green water, but didn't make it far."
            if checkLocaleMove(-1,'posX') == True:
                changeLocale(-1,'posX',currentUsername)
                giveActionPoints(currentUsername,-1)
                message = "went West"
            
            



    
    if action == "punch":
        message = ("realized there is no person named "+object+" here to punch. He punched the air in vain.")
        if sameCurrentLocation(object) != None:
            message = ("punched "+object)
            changeHealth(object, -1)
            giveActionPoints(currentUsername,-1)
            
        
    if (message != None):

        if last_turn == True:
            changeTurn()
    else:
        message = "fooled around."
            
        
        
            
    return message
        
def changeHealth(who, amount):
    db = get_db()
    db.execute(
                'UPDATE user SET health = health + ? WHERE username = ?',
                (amount, who),
            )
    db.commit()

    return

def changeLocale(amount,direction,who):
    

    if direction == 'posY':
        db = get_db()
        db.execute(
                    'UPDATE user SET posY = posY + ? WHERE username = ?',
                    (amount,who),
                )
        db.commit()

    if direction == 'posX':
        db = get_db()
        db.execute(
                    'UPDATE user SET posX = posX + ? WHERE username = ?',
                    (amount,who),
                )
        db.commit()
    
    return

def checkLocaleMove(amount,direction):
    click.echo(str((int(g.user[direction]) + amount)))
    if ((int(g.user[direction]) + amount) > -1) and (int(g.user[direction]) + amount) < gridSize:
        
        return True

    return False

