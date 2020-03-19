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


def get_salt(username):
    db.connect()
    cursor=db.cursor()
    query = ("SELECT password from users WHERE username =\"" + username + "\"")
    salt=None
    try:
        cursor.execute(query)
        password_hash = cursor.fetchall()
        if (len(password_hash)):
            hash=password_hash[0][0]
            salt=hash[-5:]
            #hash_list=hash.split(":")
            #salt=hash_list[1]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return salt


def set_logger(ipAdress, username, password, dateTime, description):
    """
    Retreive all registrered users from the database
        :return: users
    """
    db.connect()
    cursor = db.cursor()
    query = f"INSERT INTO log VALUES ('{ipAdress}', '{username}', '{password}', '{dateTime}', '{description}')"
    get_query = "Select * from log"

    #query = 'INSERT INTO log values("105601", "warsa", "password", "dateTime", "description")'
    try:
        cursor.execute(query)
        db.commit()
        cursor.execute(get_query)
        log = cursor.fetchall()

    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        log = None
        exit(1)

    finally:
        cursor.close()
        db.close()
    return log


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
    """
        Change password for username
            :param username: The username
            :param new_password: The new password
    """
    userid = get_user_id_by_name(username)

    db.connect()
    cursor = db.cursor()

    query = ("UPDATE users SET password=\"" + new_password + "\" WHERE userid=" + str(userid))

    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("ERROR")
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()


def get_wrong_login_count(userid):
    db.connect()
    cursor = db.cursor()
    query = f"SELECT wrong_login_count from login_attempts WHERE userid ={userid}"
    #query = ("SELECT wrong_login_count from login_attempts WHERE userid =\"" + userid + "\"")
    wrong_login_count = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()

        if len(result):
            wrong_login_count = result[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return wrong_login_count


def set_wrong_login_count(userid, count, is_init):
    db.connect()
    cursor = db.cursor()
    if is_init:
        query = f"INSERT INTO login_attempts VALUES ({userid}, {count})"
    else:
        query = f"UPDATE login_attempts SET wrong_login_count={count} WHERE userid={userid}"
    try:
        cursor.execute(query)
        db.commit()
        wrong_login_count = get_wrong_login_count(userid)
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        wrong_login_count = None
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return wrong_login_count


def increment_wrong_login_count(userid):
    db.connect()
    cursor = db.cursor()
    query = f"UPDATE login_attempts SET wrong_login_count = wrong_login_count + 1 WHERE userid={userid}"
    #query = ("UPDATE login_attempts SET wrong_login_count = wrong_login_count + 1 WHERE (userid=\"" + userid + "\")")
    try:
        cursor.execute(query)
        db.commit()
        wrong_login_count = get_wrong_login_count(userid)
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        wrong_login_count = None
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return wrong_login_count



