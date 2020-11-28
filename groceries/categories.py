import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from groceries.db import get_db
bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route('', methods=('GET',))
def index():
    return render_template('categories/index.html', categories=categories())

@bp.route('', methods=('POST',))
def create():
    if request.method == 'POST':
        category_name = request.form['category_name'].strip()
        db = get_db()
        error = None

        if not category_name:
            error = 'Category Name is required.'
        elif db.execute(
            'SELECT id FROM categories WHERE name = ?', (category_name,)
        ).fetchone() is not None:
            error = 'Category {} is already listed.'.format(category_name)

        if error is None:
            db.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
            db.commit()
            flash('Created new category, "{}"'.format(category_name))
        else:
            flash(error)

    return render_template('categories/index.html', categories=categories())

@bp.route('/<int:id>', methods=('GET', 'POST'))
def update(id):
    category = get_category(id)
    return render_template('categories/update.html', category=category)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_category(id)
    db = get_db()
    db.execute('DELETE FROM categories WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('categories.index'))

def categories():
  db = get_db()
  return db.execute(
    'SELECT I.id, name'
    ' FROM categories I'
    ' ORDER BY name DESC'
  ).fetchall()

def get_category(id):
    category = get_db().execute(
        'SELECT I.id, name'
        ' FROM categories I'
        ' WHERE I.id = ?',
        (id,)
    ).fetchone()

    return category