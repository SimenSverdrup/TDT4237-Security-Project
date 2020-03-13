from models.database import db
import mysql.connector

def get_users():
    """
    Retreive all registrered users from the database
        :return: users
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid, username from users")
    try:
        cursor.execute(query)
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        users = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return users

def get_user_id_by_name(username):
    """
    Get the id of the unique username
        :param username: Name of the user
        :return: The id of the user
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid from users WHERE username =\"" + username + "\"")
    
    userid = None
    try:
        cursor.execute(query)
        users = cursor.fetchall()
        if(len(users)):
            userid = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return userid

def get_user_name_by_id(userid):
    """
    Get username from user id
        :param userid: The id of the user
        :return: The name of the user
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT username from users WHERE userid =\"" + userid + "\"")
    username = None
    try:
        cursor.execute(query)
        users = cursor.fetchall()
        if len(users):
            username = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return username

def match_user(username, password):
    """
    Check if user credentials are correct, return if exists

        :param username: The user attempting to authenticate
        :param password: The corresponding password
        :type username: str
        :type password: str
        :return: user
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid, username from users where username = \"" + username + 
            "\" and password = \"" + password + "\"")
    user = None
    try:
        cursor.execute(query)
        users = cursor.fetchall()
        if len(users):
            user = users[0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return user


def change_password(username, new_password):
    db.connect()
    cursor = db.cursor()
    query = ("UPDATE users SET password=PASSWORD('"
             + new_password + "') WHERE username='"
             + username + "'")

    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        exit(1)
    finally:
        cursor.close()
        db.close()

    ################# TESTING IF PASSWORD IS ACTUALLY UPDATED ##################
    print(query)
    db.connect()
    cursor = db.cursor()

    query = ("SELECT password from users WHERE username =\"" + username + "\"")
    pw = ''
    try:
        cursor.execute(query)
        pws = cursor.fetchall()
        if len(pws):
            pw = pws[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        exit(1)
    finally:
        cursor.close()
        db.close()

    print("New password: " + pw)
    

