from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db


import click
import random

class follower:
  def __init__(self, username, health, max_health, action_points, room, kind, visible=1, alive=1, canAct=1, mood="normal", posX=0, posY=0 ):
    self.username = username
    self.health = health
    self.action_points = action_points
    self.posX = posX
    self.posY = posY
    self.max_health = max_health
    self.room = room
    self.kind = kind
    self.mood = mood
    self.canAct = canAct
    self.alive = alive
    self.visible = visible


dalmation = follower('dalmation',6,6,3,1,"")
all_followers = [dalmation]

def getAllFollowers():
   
   return all_followers
def spawnFollower(which, where, whoseUsername):


    db = get_db()
    db.execute(
        "INSERT INTO user (username, password, kind, posX, posY) VALUES (?, ?, ?, ?, ?)",
        (which.username, '123', whoseUsername, where['posX'], where['posY']),
    )
    db.commit()

def killUser(username):


    db = get_db()

    db.execute(
        'UPDATE user SET mood = ?, canAct = 0, alive = 0 WHERE username = ?', ('dead',username),
        
    )
    db.commit()


   

   
