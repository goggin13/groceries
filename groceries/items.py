import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from groceries.db import get_db
bp = Blueprint('items', __name__, url_prefix='/items')

@bp.route('', methods=('GET',))
def index():
    return render_template('items/index.html', items=items())

@bp.route('', methods=('POST',))
def create():
    if request.method == 'POST':
        item_name = request.form['item_name'].strip()
        db = get_db()
        error = None

        if not item_name:
            error = 'Item Name is required.'
        elif db.execute(
            'SELECT id FROM items WHERE name = ?', (item_name,)
        ).fetchone() is not None:
            error = 'Item {} is already listed.'.format(item_name)

        if error is None:
            db.execute('INSERT INTO items (name) VALUES (?)', (item_name,))
            db.commit()
            flash('Created new item, "{}"'.format(item_name))
        else:
            flash(error)

    return render_template('items/index.html', items=items())

@bp.route('/<int:id>', methods=('GET', 'POST'))
def update(id):
    item = get_item(id)
    return render_template('items/update.html', item=item)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_item(id)
    db = get_db()
    db.cursor().execute('DELETE FROM items WHERE id = %s', (id,))
    db.commit()
    return redirect(url_for('items.index'))

def items():
  cursor = get_db().cursor()
  cursor.execute(
    'SELECT I.id, name'
    ' FROM items I'
    ' ORDER BY name DESC'
  )
  results = cursor.fetchall()

  return map(tuple_to_dict, results)

def get_item(id):
    cursor = get_db().cursor()
    cursor.execute(
        'SELECT I.id, name'
        ' FROM items I'
        ' WHERE I.id = %s;',
        (id,)
    )
    item = cursor.fetchone()

    return tuple_to_dict(item)

def tuple_to_dict(item):
    return {"id": item[0], "name": item[1]}

