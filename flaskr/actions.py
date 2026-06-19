from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db
from flaskr.turns import giveActionPoints, changeTurn, checkTurn
from flaskr.enemies import spawnEnemy, getAllEnemies, killUser
from flaskr.followers import getAllNPCs, spawnFollower, getAllFollowers, isFollower
import click
import random
import time

gridSize = 5

def giveAllActions(who):

    base_actions = ["move","punch","take","drop","give","spawn","sit"]

    match who['mood']:

        case "sitting":
            base_actions.remove("move")
            base_actions.append("rise")
        
    
    if getInventory(who):

        for q in getInventory(who):
            
            name = get_db().execute(
            'SELECT action FROM item WHERE id = ?', (q['id'],)
            ).fetchone()[0]

            base_actions.append(name)
    
    if getAllFollowers(who['username']):
            base_actions.append("command")




    placeAction = getLocale(getUserLocationID(who))['action']

    if placeAction != "None":
            base_actions.append(placeAction)
    return base_actions
            

    



def canAction(action,who):

    for q in giveAllActions(who):
        if q == action:
            return True
    return False


def sameCurrentLocation(username,username2):

    user_detail = get_db().execute(
            'SELECT * FROM user WHERE username = ? AND alive = 1', (username,)
            ).fetchone()
    
    if user_detail == None:
        return False

    user_detail2 = get_db().execute(
            'SELECT id FROM user WHERE posX = ? AND posY = ? AND username = ? AND alive = 1', (user_detail['posX'], user_detail['posY'], username2,)
            ).fetchone()
    if user_detail2 == None:
        return False
    
    return True
def allSameLocation(who):

    guys = []
    targets = get_db().execute(
        'SELECT * FROM user WHERE posX = ? AND posY = ?', (who['posX'], who['posY'])
     ).fetchall()
    
    for q in targets:
        if q['username'] != who['username']:
            guys.append(q)
    return guys

def targetUsernames(who):
    
    targets = []
    for q in allSameLocation(who):
        if (q['alive'] == 1) or (q['canAct'] == 1):
            targets.append(q['username'])
    return targets
    
    
def takeAction(full_name,whom,describe):
    
    message = "fooled around."
    name = full_name.split()
    action = name[0].lower()
    subjects = name[1:]
    object = None
    if subjects != []:
        object = subjects[0]
    last_turn = False
    acted = False
    currentUsername = whom['username']


    if (int(whom['action_points']) < 1):
        return 'It is not your turn.'
    if checkTurn() != int(whom['id']) and describe != "Coordinated action is the new joy, so they say.":
        return 'It is not your turn.'
    if canAction(action,whom) == False:
        return 'You cannot do that.'
    
       
        
    if action == "sleep":
        last_turn = True
        giveActionPoints(currentUsername, -(int(whom['action_points'])))
        changeMood(currentUsername, "normal")
        acted = True
        message = "slept fast and hard: surrendering their body to the ground."

    if action == "sit":
        last_turn = True
        giveActionPoints(currentUsername, -(int(whom['action_points'])))
        changeMood(currentUsername, "sitting")
        acted = True
        message = "sat down"

    if action == "rise":
        
        giveActionPoints(currentUsername, -1)
        changeMood(currentUsername, "normal")
        acted = True
        message = "rose to his feet"

    if action == "spawn":
        acted = False
        if object != None:
            spawnEnemy(getAllEnemies()[0],g.location)
        else:
            spawnFollower(getAllNPCs()[0],g.location,currentUsername)

    if len(subjects) == 1:

        if action == "move":
            
            if object == "north":
                
                
                message = "cannot go that way"
                if checkLocaleMove(1,'posY',whom) == True:
                    changeLocale(1,'posY',currentUsername)
                    giveActionPoints(currentUsername,-1)
                    message = "went North"
                    acted = True

            if object == "south":
                
                
                message = "cannot go that way"
                if checkLocaleMove(-1,'posY',whom) == True:
                    changeLocale(-1,'posY',currentUsername)
                    giveActionPoints(currentUsername,-1)
                    message = "went South"
                    acted = True
            
            if object == "east":
                
                
                message = "cannot go that way"
                if checkLocaleMove(1,'posX',whom) == True:
                    changeLocale(1,'posX',currentUsername)
                    giveActionPoints(currentUsername,-1)
                    message = "went East"
                    acted = True

            if object == "west":
                
                
                message = "cannot go that way"
                if checkLocaleMove(-1,'posX',whom) == True:
                    changeLocale(-1,'posX',currentUsername)
                    giveActionPoints(currentUsername,-1)
                    message = "went West"
                    acted = True
            
            if acted == True and getAllFollowers(currentUsername) != None:
                for q in getAllFollowers(currentUsername):

                    takeAction(full_name, q, "Coordinated action is the new joy, so they say.")
                
                

        if action == "punch":
            
            message = ("realized there is no person named "+object+" here to punch. He punched the air in vain.")
            if sameCurrentLocation(object,currentUsername) == True:
                changeHealth(object, -1)
                giveActionPoints(currentUsername,-1)
                acted = True
                if getUserHealth(object) <= 0:
                    message = ("punched and killed "+object+". A heart's screen is it's hands it seems.")
                    dropInventory(object)
                    killUser(object)
                else:
                    message = ("punched "+object)


        if action == "stab":
            message = ("realized there is no person named "+object+" here to stab. He stabbed at the whistling air in vain.")
            if sameCurrentLocation(object,currentUsername) == True:
                
                changeHealth(object, -2)
                giveActionPoints(currentUsername,-1)
                acted = True
                if getUserHealth(object) <= 0:
                    message = ("stabbed and killed "+object+". A heart's screen is it's hands it seems.")
                    killUser(object)
                    dropInventory(object)
                else:
                    message = ("stabbed "+object)




        if action == "take":
            message = "thought he could take the uh thing"
            item = getItemPlace(object)
            
            if (str(item[0]) == str(getUserLocationID(whom))) and (item[1] == 1):
                message = "didn't have room on his person for the "+object
                
                
                
                                
                if  whom['room'] > len(getInventory(whom)):
                    message = "picked up the "+object
                    putItem(object, 'user', currentUsername)
                    giveActionPoints(currentUsername,-1)
                    acted = True

        if action == "drop":
            message = "thought he could drop the "+object
            item = getItemPlace(object)
            
            if (str(item[0]) == str(whom['id'])) and (item[1] == 0):
                message = "dropped the "+object
                
                putItem(object, 'location', getUserLocationID(whom))
                giveActionPoints(currentUsername,-1)


    
    if len(subjects) == 2:
        
        if action == "give":
            reciever = getUser(subjects[0])
            item = getItemPlace(subjects[1])
            message = "thought he could drop the "+reciever['username']
            if  (str(item[0]) == str(whom['id'])) and (item[1] == 0) and (reciever['room'] > len(getInventory(reciever))):
                message = "gave the "+subjects[1]+" to "+reciever['username']
                putItem(subjects[1], 'user', reciever['username'])
                giveActionPoints(currentUsername,-1)
                acted = True
    
    if action == "command":
        obeyer = object

        subjects.remove(object)

        command = ' '.join(subjects)
        message = "attempted to command someone who doesn't respect him"
        if  isFollower(obeyer,currentUsername) == True :
            message = "told "+obeyer+" something but wasn't able to yell it far enough."
            if sameCurrentLocation(currentUsername,obeyer) == True:
                message = "told "+obeyer+" to do the impossible"
                if takeAction(command,getUser(obeyer),"Coordinated action is the new joy, so they say.") != ('It is not your turn.' or 'You cannot do that.'):
                    message = "simply commanded it."
                    acted = False
        

        





    if (message != "fooled around.") and (message != "cannot go that way"):

        db = get_db()
        db.execute(
            'INSERT INTO act (turn_action, author_id, turn_description)'
            ' VALUES (?, ?, ?)',
            (message, whom['id'], describe)
        )
        db.commit()
        click.echo("action and message recorded")
        click.echo(str(whom['kind']))
        if (int(whom['action_points']) == 1) and (whom['kind'] == 'player' or whom['kind'] == 'hostile'):
            last_turn = True
            click.echo("is last turn: yes")
        if last_turn == True and acted == True and (whom['kind'] == 'player' or whom['kind'] == 'hostile'):
            changeTurn()
            
        
        
            
    return message
        
def changeHealth(username, amount):
    db = get_db()
    db.execute(
                'UPDATE user SET health = health + ? WHERE username = ?',
                (amount, username),
            )
    db.commit()

    return

def changeLocale(amount,direction,username):
    

    if direction == 'posY':
        db = get_db()
        db.execute(
                    'UPDATE user SET posY = posY + ? WHERE username = ?',
                    (amount,username),
                )
        db.commit()

    if direction == 'posX':
        db = get_db()
        db.execute(
                    'UPDATE user SET posX = posX + ? WHERE username = ?',
                    (amount,username),
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
    
    if theItem != None:
        return [theItem['ownerID'],theItem['onGround']]

def putItem(itemName, ownerType, IDusername):

    theItem = get_db().execute(
            'SELECT * FROM item WHERE full_name = ?', (itemName,)
            ).fetchone()
    value = 0
    if ownerType == 'location':
        value = 1
        db = get_db()
        db.execute(
            'UPDATE item SET ownerID = ?, onGround = ? WHERE id = ?', (IDusername, value, theItem['id']),
            )
        db.commit()
        return
    
    db = get_db()
    db.execute(
        'UPDATE item SET ownerID = ?, onGround = ? WHERE id = ?', (getUser(IDusername)['id'], value, theItem['id']),
        )
    db.commit()
    return 

def getInventory(who):

    inventory = []
    getter = get_db().execute(
        'SELECT * FROM item WHERE ownerID = ? AND onGround = 0', (who['id'],)
            
        ).fetchall()
    
    for q in getter:
        inventory.append(q)
    
    return inventory

def getUserLocationID(who):

    location = get_db().execute(
    'SELECT * FROM location WHERE posX = ? AND posY = ?', (who['posX'],who['posY'])
        
    ).fetchone()

    return location['id']

def getUserHealth(username):

    location = get_db().execute(
    'SELECT health FROM user WHERE username = ?', (username,)
        
    ).fetchone()

    return int(location[0])

def dropInventory(username):

    who = get_db().execute(
    'SELECT * FROM user WHERE username = ?', (username,)
        
    ).fetchone()

    for q in getInventory(who):
        putItem(q['full_name'],'location',getUserLocationID(who))

def getUser(username):
    location = get_db().execute(
    'SELECT * FROM user WHERE username = ?', (username,)
        
    ).fetchone()
    return location

def getLocale(id):
    location = get_db().execute(
    'SELECT * FROM location WHERE id = ?', (id,)
        
    ).fetchone()
    return location

def changeMood(username, mood):

    db = get_db()

    db.execute(
        'UPDATE user SET mood = ? WHERE username = ?',
        (mood, username)
    )
    db.commit()

    return

def hostileTurn(hostile):

    


    
    
    while hostile['action_points'] > 0:
        click.echo("While: Enemy currently has: "+str(hostile['action_points'])+" action points")
        time.sleep(1)
        if targetUsernames(hostile) == []:
            changeTurn()
            killUser(hostile['username'])
            return None
        

        hostile = get_db().execute(
        'SELECT * FROM user WHERE username = ?', (hostile['username'],)
        ).fetchone()

        

        if hostile != None:
        
            turn_action = "punch "+str(random.choice(targetUsernames(hostile)))
            
            click.echo("hostile try")
            action_message = takeAction(turn_action, hostile, "My anger steams. If my claws don't harm, I hope this will sharpen them.")

    return action_message



