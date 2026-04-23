from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db
from flaskr.turns import giveActionPoints, changeTurn, checkTurn

import click

gridSize = 2

def giveAllActions(who):
    base_actions = ["move","punch","take","drop"]
    
    if getInventory(who):

        for q in getInventory(who):
            
            name = get_db().execute(
            'SELECT action FROM item WHERE id = ?', (q['id'],)
            ).fetchone()[0]

            base_actions.append(name)
            

    

    all_actions = base_actions
    click.echo(all_actions)
    return all_actions

def canAction(action,who):

    for q in giveAllActions(who):
        if q == action:
            return True
    return False


def sameCurrentLocation(username,username2):

    user_detail = get_db().execute(
            'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

    user_detail2 = get_db().execute(
            'SELECT id FROM user WHERE posX = ? AND posY = ? AND username = ?', (user_detail['posX'], user_detail['posY'], username2,)
            ).fetchone()
    
    click.echo(user_detail2)
    return user_detail



def takeAction(full_name,whom):
    
    message = None
    name = full_name.split()
    action = name[0].lower()
    last_turn = False
    currentUsername = whom['username']
    if len(name) > 1:
        object = name[1]

    if (int(whom['action_points']) < 1) or checkTurn() != int(whom['id']):
        return 'It is not your turn.'
    if canAction(action,whom) == False:
        return 'You cannot do that.'
    if int(whom['action_points']) == 1:
        last_turn = True
        



    if action == "move":
        object = object.lower()
        if object == "north":
            
            
            message = "tried to wade into the black water, but didn't make it far."
            if checkLocaleMove(1,'posY',whom) == True:
                changeLocale(1,'posY',currentUsername)
                giveActionPoints(currentUsername,-1)
                message = "went North"

        if object == "south":
            
            
            message = "tried to wade into the yellow water, but didn't make it far."
            if checkLocaleMove(-1,'posY',whom) == True:
                changeLocale(-1,'posY',currentUsername)
                giveActionPoints(currentUsername,-1)
                message = "went South"
        
        if object == "east":
            
            
            message = "tried to wade into the pink water, but didn't make it far."
            if checkLocaleMove(1,'posX',whom) == True:
                changeLocale(1,'posX',currentUsername)
                giveActionPoints(currentUsername,-1)
                message = "went East"

        if object == "west":
            
            
            message = "tried to wade into the green water, but didn't make it far."
            if checkLocaleMove(-1,'posX',whom) == True:
                changeLocale(-1,'posX',currentUsername)
                giveActionPoints(currentUsername,-1)
                message = "went West"
            
            

    if action == "punch":
        
        message = ("realized there is no person named "+object+" here to punch. He punched the air in vain.")
        if sameCurrentLocation(object,currentUsername) != None:
            message = ("punched "+object)
            changeHealth(object, -1)
            giveActionPoints(currentUsername,-1)

    if action == "stab":
        message = ("realized there is no person named "+object+" here to stab. He stabbed at the whistling air in vain.")
        if sameCurrentLocation(object,currentUsername) != None:
            message = ("stabbed "+object)
            changeHealth(object, -2)
            giveActionPoints(currentUsername,-1)


    if action == "take":
        message = "thought he could take the uh thing"
        item = getItemPlace(object)
        
        if (str(item[0]) == str(getUserLocationID(whom))) and (item[1] == 1):
            message = "didn't have room on his person for the "+object
            
            
            
                         
            if  whom['room'] > len(getInventory(whom)):
                message = "picked up the "+object
                putItem(object, 'user', whom['id'])
                giveActionPoints(currentUsername,-1)

    if action == "drop":
        message = "thought he could drop the "+object
        item = getItemPlace(object)
        
        if (str(item[0]) == str(whom['id'])) and (item[1] == 0):
            message = "dropped the "+object
            
            putItem(object, 'location', getUserLocationID(whom))
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

def checkLocaleMove(amount,direction, who):
    
    if ((int(who[direction]) + amount) > -1) and (int(who[direction]) + amount) < gridSize:
        
        return True

    return False

def getItemPlace(itemName):

    theItem = get_db().execute(
            'SELECT * FROM item WHERE full_name = ?', (itemName,)
            ).fetchone()
    
    return [theItem['ownerID'],theItem['onGround']]

def putItem(itemName, ownerType, ownerID):

    theItem = get_db().execute(
            'SELECT * FROM item WHERE full_name = ?', (itemName,)
            ).fetchone()
    value = 0
    if ownerType == 'location':
        value = 1

    
    db = get_db()
    db.execute(
        'UPDATE item SET ownerID = ?, onGround = ? WHERE id = ?', (ownerID, value, theItem['id']),
        )
    db.commit()
    return False

def getInventory(who):

    inventory = []
    getter = get_db().execute(
        'SELECT * FROM item WHERE ownerID = ? AND onGround = 0', (who['id'],)
            
        ).fetchall()
    
    for q in getter:
        inventory.append(q)
    click.echo(str(inventory))
    return inventory

def getUserLocationID(who):

    location = get_db().execute(
    'SELECT * FROM location WHERE posX = ? AND posY = ?', (who['posX'],who['posY'])
        
    ).fetchone()

    return location['id']



