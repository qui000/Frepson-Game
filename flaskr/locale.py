from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


import click



class place:
  def __init__(self, full_name, posX, posY):
    self.full_name = full_name
    self.posX = posX
    self.posY = posY


startingHole = place('Starting Hole', 0, 0)
brook = place('The Brook', 1, 0)
puddle = place('The Puddle Library', 0, 1)
haystack = place('The Musty Haystack', 1, 1)

all_locations = {startingHole, brook, puddle, haystack}

def giveLocations():
   
   return all_locations






    
