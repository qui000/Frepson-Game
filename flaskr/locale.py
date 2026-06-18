from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


import click



class place:
  def __init__(self, full_name, posX, posY, action="None", fencedID=0, structure=0, structureOwnerID=0):
    self.full_name = full_name
    self.posX = posX
    self.posY = posY
    self.action = action
    self.fencedID = fencedID
    self.structure = structure
    self.structureOwnerID = structureOwnerID


startingPath = place('Little Clearing', 0, 0)
secondPath = place('Eastward Path', 1, 0)
thirdPath = place('Signed Path: Spencward Manor', 2, 0)
fourthPath = place('Path Along A Garden', 3, 0)
fifthPath= place('Path Curving Northward', 4, 0)
grandPorch = place('The Grand Porch', 4, 1)
groomedGarden = place('Groomed Garden', 3, 1)
swampyThicket = place('Swampy Thicket', 2, 1)
slimyThicket = place('Slimy Thicket', 1, 1)
coolPool = place('Cool Pool', 0, 1)
fisherShack = place('The Fishing Shack', 0, 2)
bottomWood = place('Shady Wood', 1, 2)
field1 = place('Field of Green Berries', 2, 2)
field2 = place('Field of Tangy Spices', 3, 2)
manor1 = place('The Manor Dining Room', 4, 2)
manor2 = place('The Manor Kitchen', 4, 3)
field3 = place('Orchard of Yellow Cork Fruits', 3, 3)
field4 = place('The Brook', 2, 3)
middleWood = place('The Very Dark Wood', 1, 3)
waterfall = place('The Cave Waterfall', 0, 3)
cave = place('The Cave', 0, 4)
topWood = place('A Sparce Wood', 1, 4)
barracks = place('A Line of Little Huts', 2, 4)
manorToolshed = place('Manor Toolshed', 3, 4, "sleep")
manor3 = place('The Manor Library', 4, 4)


all_locations = {startingPath, secondPath, thirdPath, fourthPath, fifthPath,
                 grandPorch, groomedGarden, swampyThicket, slimyThicket, coolPool,
                 fisherShack, bottomWood, field1, field2, manor1, 
                 manor2, field3, field4, middleWood, waterfall,
                 cave, topWood, barracks, manorToolshed, manor3
                 
                 
                 
                 
                 }

def giveLocations():
   
   return all_locations






    
