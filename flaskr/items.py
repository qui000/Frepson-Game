from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


import click



class item:
  def __init__(self, full_name, health, action):
    self.full_name = full_name
    self.health = health
    self.action = action

 

knife = item('knife', 8, 'stab')
needle = item('needle', 1, 'stick')
rock = item('rock', 10, 'throw')

all_items = [knife, needle, rock]

def giveItems():
   
   return all_items



    
