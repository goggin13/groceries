import pytest
from flaskr.db import get_db

def test_index_displays_items(client):
    response = client.get('/items')
    assert b'apples' in response.data
    assert b'eggs' in response.data

def test_index_displays_item_links(client):
    response = client.get('/items')
    assert b'href="/items/1"' in response.data
    assert b'href="/items/2"' in response.data

def test_creating_a_new_ingredient(client, db):
    old_count = db.execute('select count(id) from items').fetchone()[0]
    response = client.post('/items', data={'item_name': 'pizza'})
    new_count = db.execute('select count(id) from items').fetchone()[0]
    assert new_count == old_count + 1
    assert b'pizza' in response.data

def test_new_ingredient_success_message(client, db):
    response = client.post('/items', data={'item_name': 'pizza'})
    msg = 'Created new item, &#34;{}&#34;'.format("pizza")
    assert msg in str(response.data)

def test_header_shows_count_of_items(client, db):
    count = db.execute('select count(id) from items').fetchone()[0]
    response = client.get('/items')
    assert b'<title>2 Items</title>' in response.data

def test_cant_add_same_item_twice(client, db):
    old_count = db.execute('select count(id) from items').fetchone()[0]
    response = client.post('/items', data={'item_name': 'apples'})
    new_count = db.execute('select count(id) from items').fetchone()[0]
    assert new_count == old_count
    assert b'Item apples is already listed.' in response.data

def test_item_name_is_required(client, db):
    old_count = db.execute('select count(id) from items').fetchone()[0]
    response = client.post('/items', data={'item_name': ''})
    new_count = db.execute('select count(id) from items').fetchone()[0]
    assert new_count == old_count
    assert b'Item Name is required' in response.data

def test_blank_item_names_are_rejected(client, db):
    old_count = db.execute('select count(id) from items').fetchone()[0]
    response = client.post('/items', data={'item_name': ' '})
    new_count = db.execute('select count(id) from items').fetchone()[0]
    assert new_count == old_count
    assert b'Item Name is required' in response.data
