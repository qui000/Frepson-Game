from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


import click



class place:
  def __init__(self, full_name, posX, posY, ground='', npc='', enemy=''):
    self.full_name = full_name
    self.posX = posX
    self.posY = posY
    self.ground = ground
    self.npc = npc
    self.enemy = enemy

startingHole = place('Starting Hole', 0, 0, 1)
brook = place('The Brook', 1, 0, 3)
puddle = place('The Puddle Library', 0, 1,)
haystack = place('The Musty Haystack', 1, 1, 2)

all_locations = {startingHole, brook, puddle, haystack}

def giveLocations():
   
   return all_locations






    
