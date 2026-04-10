from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db


def giveAllActions():
    all_actions = ["move","punch"]

    return all_actions


def checkCurrentUser(for_what):

    user_detail = get_db().execute(
            'SELECT ? FROM user WHERE id = ?', (for_what, g.user['id'],)
            ).fetchone()
    

    return user_detail

def checkForSame(for_what, username):

    user_detail = get_db().execute(
            'SELECT ? FROM user WHERE locale = ? AND username = ?', (for_what, g.user['locale'], username,)
            ).fetchone()
    

    return user_detail



def takeAction(full_name):

    name = full_name.split()
    action = name[0]
    if len(name) > 1:
        object = name[1]

    if action == "move":
        db = get_db()
        db.execute(
                    'UPDATE user SET locale = locale + 1 WHERE id = ?',
                    (g.user['id'],),
                )
        db.commit()
        return("moved")
    
    if action == "punch":

        punch = checkForSame('username', object)

        if punch != None:
            db = get_db()
            db.execute(
                        'UPDATE user SET health = health - 1 WHERE username = ?',
                        (object,),
                    )
            db.commit()
            return("punched "+object)
        
            
        return("realized there is no person named "+object+" here to punch. He punches the air in vain")
    
    return None
        

