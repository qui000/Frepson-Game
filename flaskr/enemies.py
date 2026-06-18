from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db


import click
import random

class enemy:
  def __init__(self, username, health, max_health, action_points, max_action_points, room, visible=1, alive=1, canAct=1, mood="normal", kind="hostile", posX=0, posY=0 ):
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


bear = enemy('bear',15,25,1,6,1)
all_enemies = [bear]

def getAllEnemies():
   
   return all_enemies
def spawnEnemy(which, where):


    db = get_db()
    db.execute(
        "INSERT INTO user (username, password, kind, mood, posX, posY) VALUES (?, ?, ?, ?, ?, ?)",
        (which.username, '123', 'hostile', which.mood, where['posX'], where['posY']),
    )
    db.commit()

def killUser(username):


    db = get_db()

    db.execute(
        'UPDATE user SET mood = ?, canAct = 0, alive = 0, visible = 0 WHERE username = ?', ('dead',username),
        
    )
    db.commit()


   

   
