import pytest

from server import *

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    print(app)

    with app.test_client() as client:
        with app.app_context():
            print('blah')
        yield client

''' Test that the root route of "/" works
    so that we know that client connected properly
    in the fixture '''
def test_root(client):
    rv = client.get('/')
    assert b'Hello World' in rv.data

''' USER ENDPOINTS '''

''' Test that when we register a new user that a string
    of the userid is returned '''
def test_register(client):
    response = client.get('/register_user', data={'name': 'delta', 
                                                  'password': '1234'})
    assert b'\"USER_EXISTS\"' not in response.data 
    assert b'\"NO_DB\"' not in response.data

''' Test that when we try to register the same user that we
    get back "USER_EXISTS" '''
def test_register_existing_user(client):
    response = client.get('/register_user', data={'name': 'delta', 
                                                  'password': '1234'})
    assert b'\"USER_EXISTS\"' in response.data 

''' Test that when we try to authenticate an existing user 
    with the correct username and password that we
    get back a string of their userid '''
def test_authenticate_user_success(client):
    response = client.get('/authenticate_user', data={'name': 'delta', 
                                                  'password': '1234'})
    assert b'\"USER_DNE\"' not in response.data 
    assert b'\"NO_DB\"' not in response.data
    assert b'\"INCORRECT_PASSWORD\"' not in response.data 

''' Test that when we try to authenticate an existing user 
    with the wrong password that we get back the string 
    of "INCORRECT PASSWORD" '''
def test_authenticate_user_wrong_password(client):
    response = client.get('/authenticate_user', data={'name': 'delta', 
                                                  'password': '1235'})
    assert b'\"INCORRECT_PASSWORD\"' in response.data 

''' Test that when we try to authenticate an non-existing user 
    that we get back the string of "USER_DNE" '''
def test_authenticate_user_no_user(client):
    response = client.get('/authenticate_user', data={'name': 'cpen', 
                                                  'password': '391'})
    assert b'\"USER_DNE\"' in response.data 

''' Test that when we try to delete an existing user with incorrect
    incorrect password that we get back the string of "FAILED" '''
def test_delete_fail(client):
    response = client.get('/delete_user', data={'name': 'delta', 
                                                  'password': '391'})
    assert b'\"FAILED\"' in response.data

''' Test that when we try to delete an existing user with incorrect
    password that we get back the string of "INCORRECT_PASSWORD" '''
def test_delete_wrong_password(client):
    response = client.get('/delete_user', data={'name': 'delta', 
                                                  'password': '391'})
    assert b'\"INCORRECT_PASSWORD\"' in response.data

''' Test that when we try to delete an existing user with correct
    password that we get back the string of "SUCCESS" '''
def test_delete_success(client):
    response = client.get('/delete_user', data={'name': 'delta', 
                                                  'password': '1234'})
    assert b'\"SUCCESS\"' in response.data

''' Test that when we try to delete a non-existing user 
    that we get back the string of "USER_DNE" '''
def test_delete_no_user(client):
    response = client.get('/delete_user', data={'name': 'delta', 
                                                  'password': '1234'})
    assert b'\"USER_DNE\"' in response.data

''' HISTORY ENDPOINTS '''