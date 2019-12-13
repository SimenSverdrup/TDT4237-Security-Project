from models.database import db

def get_users():
    """
    Retreive all registrered users from the database
        :return: users
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid, username from users")
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    return users

def get_user_id_by_name(username):
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid from users WHERE username =\"" + username + "\"")
    cursor.execute(query)
    try:
        userid = cursor.fetchall()[0][0]
    except:
        userid = None
    cursor.close()
    return userid

def get_user_name_by_id(userid):
    db.connect()
    cursor = db.cursor()
    query = ("SELECT username from users WHERE userid =\"" + userid + "\"")
    cursor.execute(query)
    try:
        username = cursor.fetchall()[0][0]
    except:
        username = None
    cursor.close()
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
    cursor.execute(query)
    try:
        user = cursor.fetchall()[0]
    except:
        user = None
    cursor.close()
    return user
