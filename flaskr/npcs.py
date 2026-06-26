from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)




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

#Followers

dalmation = NPC('dalmation',6,6,3,"")
puppy = NPC('puppy',2,2,1,"")

#Dinos

triceratops = NPC('triceratops',400,400,10,"patron",10,10,1,1,0,"normal",4,1)



all_NPCs = [dalmation]
staticNPCs = []
activeNPCs = []
followers = [dalmation]
dinos = [triceratops]
dinosons = []

startingNPCs = [triceratops]

def getAllNPCs():
   
   return all_NPCs

