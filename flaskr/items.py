from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


import click



class item:
  def __init__(self, full_name, health, action,ownerID=0,onGround=1,armorType="None"):
    self.full_name = full_name
    self.health = health
    self.action = action
    self.armorType = armorType
    self.ownerID = ownerID
    self.onGround = onGround

 

knife = item('knife', 8, 'stab',1)
needle = item('needle', 1, 'stick',2)
rock = item('rock', 10, 'throw',3)


ground_items = [knife, needle, rock]
starting_items = []



def giveItems():
   
   return ground_items



    
