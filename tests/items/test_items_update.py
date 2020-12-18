import pytest
from groceries.db import get_db, query

def test_update_displays_item(client):
    response = client.get('/items/1')
    assert b'apples' in response.data

def test_update_displays_delete_link(client):
    response = client.get('/items/1')
    assert b'action="/items/1/delete"' in response.data

def test_update_page_can_delete_an_item(client, db):
    old_count = query('select count(*) from items;')
    response = client.post('/items/1/delete', data={'item_name': 'pizza'})
    new_count = query('select count(*) from items;')
    assert new_count == old_count - 1
    assert b'apples' not in response.data
