import mongomock

from database import *

def test_add_history():
    db = mongomock.MongoClient().db
    username = 'test_user'
    history = {"history": [{"native_language": 'en',
                            "target_language": 'fr',
                            "native": 'potato',
                            "translated": 'pomme de terre'}]}

    create_user(db, username, 'test_password')
    add_history(db, username, 'en', 'fr', 'potato', 'pomme de terre')

    assert history == get_history(db, username)
    print("Add history PASSED :)")

def test_remove_history():
    db = mongomock.MongoClient().db
    username = 'test_user'
    history = {"history": [{"native_language": 'en',
                            "target_language": 'fr',
                            "native": 'potato',
                            "translated": 'pomme de terre'}]}

    create_user(db, username, 'test_password')
    add_history(db, username, 'en', 'fr', 'potato', 'pomme de terre')
    remove_history(db, username, 'en', 'fr', 'potato', 'pomme de terre')

    assert {"history": []} == get_history(db, username)
    print("Remove history PASSED :)")

def test_create_user():
    db = mongomock.MongoClient().db
    user1 = 'test_user1'
    user2 = 'test_user2'
    pw = 'test_password'

    create_user(db, user1, pw)

    assert '\"INCORRECT_PASSWORD\"' == find_user(db, user1, 'wrong_password')
    assert '\"USER_DNE\"' == find_user(db, user2, pw)
    print("Authenticate user PASSED :)")

    assert '\"INCORRECT_PASSWORD\"' != find_user(db, user1, pw)
    assert '\"USER_DNE\"' != find_user(db, user1, pw)
    print("Create user PASSED :)")


def test_remove_user():
    db = mongomock.MongoClient().db
    user1 = 'test_user1'
    user2 = 'test_user2'
    pw = 'test_password'

    create_user(db, user1, pw)
    create_user(db, user2, pw)

    assert '\"USER_DNE\"' != find_user(db, user1, pw)
    assert '\"USER_DNE\"' != find_user(db, user2, pw)

    remove_user(db, user1, pw)

    assert '\"USER_DNE\"' == find_user(db, user1, pw)
    assert '\"USER_DNE\"' != find_user(db, user2, pw)
    print("User removal PASSED :)")

if __name__ == "__main__":
    test_add_history()
    test_remove_history()
    test_create_user()
    test_remove_user()

    # If any test fails, the assert statement in that test 
    # will prevent this final print statement from executing
    print("\nALL TESTS PASSED !!! :3\n")
