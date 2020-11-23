import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
bp = Blueprint('ingredients', __name__, url_prefix='/ingredients')

def ingredients():
  db = get_db()
  return db.execute(
    'SELECT I.id, name'
    ' FROM ingredients I'
    ' ORDER BY name DESC'
  ).fetchall()

def get_ingredient(id):
    ingredient = get_db().execute(
        'SELECT I.id, name'
        ' FROM ingredients I'
        ' WHERE I.id = ?',
        (id,)
    ).fetchone()

    return ingredient

@bp.route('', methods=('GET',))
def index():
    return render_template('ingredients/index.html', ingredients=ingredients())

@bp.route('', methods=('POST',))
def create():
    if request.method == 'POST':
        ingredient_name = request.form['ingredient_name']
        db = get_db()
        error = None

        if not ingredient_name:
            error = 'Ingredient Name is required.'
        elif db.execute(
            'SELECT id FROM ingredients WHERE name = ?', (ingredient_name,)
        ).fetchone() is not None:
            error = 'Ingredient {} is already listed.'.format(ingedient_name)

        if error is None:
            db.execute('INSERT INTO ingredients (name) VALUES (?)', (ingredient_name,))
            db.commit()
            return redirect(url_for('ingredients.index'))

        flash(error)

    return render_template('ingredients/index.html', ingredients=ingredients())

@bp.route('/<int:id>', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        ingredient_name = request.form['ingredient_name']
        error = None

        if not ingredient_name:
            error = 'ingredient name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE ingredients SET name = ?'
                ' WHERE id = ?',
                (ingredient_name, id)
            )
            db.commit()

    ingredient = get_ingredient(id)
    return render_template('ingredients/update.html', ingredient=ingredient)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_ingredient(id)
    db = get_db()
    db.execute('DELETE FROM ingredients WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('ingredients.index'))
