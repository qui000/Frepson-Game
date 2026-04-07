from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db



all_actions = {"move","punch"}


def takeAction(name):

    if name == "move":
        db = get_db()
        db.execute(
                    "UPDATE user SET location = location + 1 WHERE ID = VALUE (?)",
                    (g.user['id']),
                )
        db.commit()
        return("moved")
    
    return None
        

