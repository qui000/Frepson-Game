from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


import click



class structure:
  def __init__(self, full_name, action, type, ownerID, level, posX, posY, health, max_health):
    self.full_name = full_name
    self.action = action
    self.type = type
    self.level = level
    self.posX = posX
    self.posY = posY
    self.health = health
    self.max_health = max_health
    self.action = action
    self.ownerID = ownerID


 

front_porch = structure("Porch","None","room",1,1,4,1,50,50)



starting_structures = [front_porch]



def giveStartingStructures():
   
   return starting_structures


    
