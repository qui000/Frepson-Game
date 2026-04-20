from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db
from flaskr.turns import giveActionPoints, changeTurn, checkTurn

import click

gridSize = 2

def giveAllActions():
    base_actions = ["move","punch","take","drop"]
    
    for q in [g.user['slot1'],g.user['slot2'],g.user['slot3']]:
        if q != 0:

            name = get_db().execute(
            'SELECT action FROM item WHERE id = ?', (q,)
            ).fetchone()[0]

            base_actions.append(name)
            

    

    all_actions = base_actions
    click.echo(all_actions)
    return all_actions

def canAction(action):

    for q in giveAllActions():
        if q == action:
            return True
    return False


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
    if canAction(action) == False:
        return 'You cannot do that.'
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

    if action == "stab":
        message = ("realized there is no person named "+object+" here to stab. He stabbed at the whistling air in vain.")
        if sameCurrentLocation(object) != None:
            message = ("stabbed "+object)
            changeHealth(object, -2)
            giveActionPoints(currentUsername,-1)


    if action == "take":
        message = "grabbed for the untakeable."
        pullName = get_db().execute(
            'SELECT full_name FROM item WHERE id = ?', (g.location['ground'],)
            ).fetchone()
        
        if pullName:
            pullName = pullName[0]
        if pullName == object:
            message = "couldn't find room in his pockets for the "+object
            if intoEmptySlot(currentUsername,g.location['ground']) == True:
                giveActionPoints(currentUsername, -1)
                itemGround(g.location['id'],0)
                message = 'picked up the '+object
                
    if action == "drop":
        message = "thought he could drop something he didn't even have."
        have = itemOnCurrentUser(object)

        if have != 'None':
            
            giveActionPoints(currentUsername,-1)
            if g.location['ground'] == 0:
                itemGround(g.location['id'],have['id'])
                message = "dropped the "+object
            else:
                message = "dropped the "+object+" and it broke beyond repair."
            removeItem(object,currentUsername)



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

def itemGround(where,what):
        db = get_db()
        db.execute(
                    'UPDATE location SET ground = ? WHERE id = ?',
                    (what,where),
                )
        db.commit()

def intoEmptySlot(who,what):



    try1 = get_db().execute(
            'SELECT slot1 FROM user WHERE username = ?', (who,)
            ).fetchone()
    if try1 != 0:
        db = get_db()
        db.execute(
                    'UPDATE user SET slot1 = ? WHERE username = ?',
                    (what,who),
                )
        db.commit()
        return True

    try2 = get_db().execute(
            'SELECT slot2 FROM user WHERE username = ?', (who,)
            ).fetchone()
    if try2 != 0:
        db = get_db()
        db.execute(
                    'UPDATE user SET slot2 = ? WHERE username = ?',
                    (what,who),
                )
        db.commit()
        return True

    try3 = get_db().execute(
            'SELECT slot3 FROM user WHERE username = ?', (who,)
            ).fetchone()
    if try3 != 0:
        db = get_db()
        db.execute(
                    'UPDATE user SET slot3 = ? WHERE username = ?',
                    (what,who),
                )
        db.commit()
        return True

    return False

def itemOnCurrentUser(itemName):
    if g.slot1 and itemName == g.slot1['full_name']:
        return g.slot1
    if g.slot2 and itemName == g.slot2['full_name']:
        return g.slot2
    if g.slot3 and itemName == g.slot3['full_name']:
        return g.slot3



    return 'None'

def removeItem(itemName,who):
    
    if itemName == g.slot1['full_name']:
        db = get_db()
        db.execute(
                'UPDATE user SET slot1 = 0 WHERE username = ?',
                (who,),
            )
        db.commit()
        return 

    if itemName == g.slot2['full_name']:
        db = get_db()
        db.execute(
                'UPDATE user SET slot2 = 0 WHERE username = ?',
                (who,),
            )
        db.commit()
        return

    if itemName == g.slot3['full_name']:
        db = get_db()
        db.execute(
                'UPDATE user SET slot3 = 0 WHERE username = ?',
                (who,),
            )
        db.commit()
        return

    return 'None'