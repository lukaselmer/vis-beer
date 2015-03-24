#!/usr/bin/env python

import pytest

import os
import tempfile

import vis_beer

@pytest.fixture
def client(request):
    #db_fd, vis_beer.app.config['DATABASE'] = tempfile.mkstemp()
    #vis_beer.app.config['TESTING'] = True
    client = vis_beer.app.test_client()
    #with vis_beer.app.app_context():
    #    vis_beer.init_db()

    def teardown():
        #os.close(db_fd)
        #os.unlink(vis_beer.app.config['DATABASE'])
        pass
    request.addfinalizer(teardown)

    return client

def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data
