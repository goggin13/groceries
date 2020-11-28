import pytest
from groceries.db import get_db

def test_index_displays_categories(client):
    response = client.get('/categories')
    assert b'dairy' in response.data
    assert b'produce' in response.data

def test_index_displays_categories_links(client):
    response = client.get('/categories')
    assert b'href="/categories/1"' in response.data
    assert b'href="/categories/2"' in response.data

def test_creating_a_new_category(client, db):
    old_count = db.execute('select count(id) from categories').fetchone()[0]
    response = client.post('/categories', data={'category_name': 'frozen'})
    new_count = db.execute('select count(id) from categories').fetchone()[0]
    assert new_count == old_count + 1
    assert b'frozen' in response.data

def test_new_category_success_message(client, db):
    response = client.post('/categories', data={'category_name': 'frozen'})
    msg = 'Created new category, &#34;{}&#34;'.format("frozen")
    assert msg in str(response.data)

def test_header_shows_count_of_categories(client, db):
    count = db.execute('select count(id) from categories').fetchone()[0]
    response = client.get('/categories')
    assert b'<title>2 Categories</title>' in response.data

def test_cant_add_same_category_twice(client, db):
    old_count = db.execute('select count(id) from categories').fetchone()[0]
    response = client.post('/categories', data={'item_name': 'dairy'})
    new_count = db.execute('select count(id) from categories').fetchone()[0]
    assert new_count == old_count
    assert b'Category dairy is already listed.' in response.data

def test_category_name_is_required(client, db):
    old_count = db.execute('select count(id) from categories').fetchone()[0]
    response = client.post('/items', data={'item_name': ''})
    new_count = db.execute('select count(id) from categories').fetchone()[0]
    assert new_count == old_count
    assert b'Category Name is required' in response.data

def test_blank_category_names_are_rejected(client, db):
    old_count = db.execute('select count(id) from items').fetchone()[0]
    response = client.post('/items', data={'category_name': ' '})
    new_count = db.execute('select count(id) from items').fetchone()[0]
    assert new_count == old_count
    assert b'Category Name is required' in response.data
