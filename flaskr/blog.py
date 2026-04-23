from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.actions import takeAction, giveAllActions
from flaskr.turns import giveActionPoints, checkTurn

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    acts = db.execute(
        'SELECT a.id, turn_action, turn_description, created, author_id, username'
        ' FROM act a JOIN user u ON a.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    users = db.execute(
        'SELECT id, username'
        ' FROM user'
        ' ORDER BY id ASC'
    ).fetchall()


    if g.user: 
        
        if (g.user['action_points'] == 0) and checkTurn() == int(g.user['id']):
            giveActionPoints(g.user['username'], 5)
        
        

            





    return render_template('blog/index.html', posts=posts, acts=acts, users=users)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/act', methods=('GET', 'POST'))
@login_required
def act():



        

    if request.method == 'POST':
        turn_action = request.form['turn_action']
        turn_description = request.form['turn_description']
        error = None
        
        
        if not turn_action:
            error = 'Action is required.'

        if error is not None:
            flash(error)
        else:

            action_message = takeAction(turn_action, g.user)

            if action_message == ('It is not your turn.') or action_message == ('You cannot do that.'):
                flash(action_message)
                return redirect(url_for('blog.index'))
            
            db = get_db()
            db.execute(
                'INSERT INTO act (turn_action, turn_description, author_id)'
                ' VALUES (?, ?, ?)',
                (action_message, turn_description, g.user['id'])
            )
            db.commit()
            
            return redirect(url_for('blog.index'))

    return render_template('blog/act.html',allActs = giveAllActions(g.user))


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

