from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db


import click
import random

class NPC:
  def __init__(self, username, health, max_health, room, kind, action_points=0, max_action_points=0, visible=1, alive=1, canAct=1, mood="normal", posX=0, posY=0 ):
    self.username = username
    self.health = health
    self.action_points = action_points
    self.max_action_points = max_action_points
    self.posX = posX
    self.posY = posY
    self.max_health = max_health
    self.room = room
    self.kind = kind
    self.mood = mood
    self.canAct = canAct
    self.alive = alive
    self.visible = visible


dalmation = NPC('dalmation',6,6,3,1,"follower")
puppy = NPC('puppy',2,2,1,1,"follower")







all_NPCs = [dalmation]
staticNPCs = []
activeNPCs = []
followers = []
dinos = []
dinosons = []
def getAllNPCs():
   
   return all_NPCs
def spawnFollower(which, where, whoseUsername):


    db = get_db()
    db.execute(
        "INSERT INTO user (username, password, kind, posX, posY, mood) VALUES (?, ?, ?, ?, ?, ?)",
        (which.username, '123', whoseUsername, where['posX'], where['posY'], which.mood),
    )
    db.commit()

def getAllFollowers(username):


    user_detail = get_db().execute(
            'SELECT * FROM user WHERE kind = ?', (username,)
            ).fetchall()
    return user_detail

def killUser(username):


    db = get_db()

    db.execute(
        'UPDATE user SET mood = ?, canAct = 0, alive = 0 WHERE username = ?', ('dead',username),
        
    )
    db.commit()

def isFollower(followerUsername, ownerUsername):

    for y in getAllFollowers(ownerUsername):
        if y['username'] == followerUsername:
            return True
    return False


   
