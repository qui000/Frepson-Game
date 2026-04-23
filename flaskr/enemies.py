from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db
from flaskr.turns import giveActionPoints, changeTurn, checkTurn

import click
import random

class enemy:
  def __init__(self, username, health, max_health, action_points, room, kind="player", posX=0, posY=0 ):
    self.username = username
    self.health = health
    self.action_points = action_points
    self.posX = posX
    self.posY = posY
    self.max_health = max_health
    self.room = room
    self.kind = kind


bear = enemy('bear',15,25,6,1)
all_enemies = [bear]

def getAllEnemies():
   
   return all_enemies
def spawnEnemy(which, where):


    db = get_db()
    db.execute(
        "INSERT INTO user (username, password) VALUES (?, ?)",
        (which['username'], '123'),
    )
    db.commit()

def hostileAct(which):
   
    targets = get_db().execute(
            'SELECT id FROM user WHERE posX = ? AND posY = ? AND username = ?', (g.location['posX'], g.location['posY'])
            ).fetchone()
   

   

   
