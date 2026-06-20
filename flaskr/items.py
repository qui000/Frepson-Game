from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


import click



class item:
  def __init__(self, full_name, health, action,ownerID=0, armorType="None", onGround=1):
    self.full_name = full_name
    self.health = health
    self.action = action
    self.armorType = armorType
    self.ownerID = ownerID
    self.onGround = onGround

 

knife = item('knife', 8, 'stab',1)
needle = item('needle', 1, 'stick',2)
rock = item('rock', 10, 'throw',3)
turtleShell = item('shell', 10, 'throw',3,'helmet')
hat = item('hat', 10, 'throw', 3, 'helmet')
shirt = item('shirt', 10, 'throw', 3, 'shirt')


ground_items = [knife, needle, rock, turtleShell, hat, shirt]
starting_items = []



def giveItems():
   
   return ground_items



    
