import pytest
from groceries.db import get_db

def test_update_displays_category(client):
    response = client.get('/categories/1')
    assert b'dairy' in response.data

def test_update_displays_delete_link(client):
    response = client.get('/categories/1')
    assert b'action="/items/1/delete"' in response.data

def test_update_page_can_delete_an_category(client, db):
    old_count = db.execute('select count(id) from categories').fetchone()[0]
    response = client.post('/categories/1/delete', data={'category_name': 'dairy'})
    new_count = db.execute('select count(id) from categories').fetchone()[0]
    assert new_count == old_count - 1
    assert b'dairy' not in response.data
