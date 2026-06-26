from flaskr.db import get_db

def spawnFollower(which, where, whoseUsername):


    db = get_db()
    db.execute(
        "INSERT INTO user (username, password, kind, posX, posY, mood) VALUES (?, ?, ?, ?, ?, ?)",
        (which.username, '123', "follower "+whoseUsername, where['posX'], where['posY'], which.mood),
    )
    db.commit()

def getAllFollowers(username):


    user_detail = get_db().execute(
            'SELECT * FROM user WHERE kind = ?', ("follower "+username,)
            ).fetchall()
    return user_detail

def killUser(username):


    db = get_db()

    db.execute(
        'UPDATE user SET mood = ?, canAct = 0, alive = 0 WHERE username = ?', ('dead',username),
        
    )
    db.commit()

def isFollower(followerUsername, ownerUsername):

    for y in getAllFollowers(ownerUsername):
        if y['username'] == followerUsername:
            return True
    return False


   