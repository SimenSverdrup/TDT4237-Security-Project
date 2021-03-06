import json

import web
from views.forms import login_form
import models.user
from views.utils import get_nav_bar
import os, hmac, base64, pickle
import hashlib
import logging
from datetime import datetime

# Get html templates
render = web.template.render('templates/')


class Login():

    # Get the server secret to perform signatures
    secret = web.config.get('session_parameters')['secret_key']
    logging.basicConfig( format=' %(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')



    def GET(self):
        """
        Show the login page
            
            :return: The login page showing other users if logged in
        """
        session = web.ctx.session
        nav = get_nav_bar(session)

        # Log the user in if the rememberme cookie is set and valid
        self.check_rememberme()

        return render.login(nav, login_form, "")

    def POST(self):
        """
        Log in to the web application and register the session
            :return:  The login page showing other users if logged in
        """

        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(username="", password="", remember=False)

        # Validate login credential with database query
        user = None
        userid = models.user.get_user_id_by_name(data.username)
        if userid:
            salt = models.user.get_salt(data.username)
            if len(salt) > 0:
                password_hash = hashlib.sha512(salt.encode('utf-8') + data.password.encode('utf-8')).hexdigest() + salt
                user = models.user.match_user(data.username, password_hash)

        # Increment counter for wrong password if user exists but wrong password
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if userid and not user:
            wrong_login_count = models.user.get_wrong_login_count(userid)
            # Making a log for every fail attempt
            userid = models.user.get_user_id_by_name(data.username)
            # if first time wrong password, initialize counter
            if wrong_login_count is None:
                 models.user.set_wrong_login_count(userid, 1, True)
                 log = models.user.set_logger(web.ctx['ip'], data.username, data.password, dt_string, "Logging failed")
                 return render.login(nav, login_form, "User authentication failed.")
            # Check if max wrong login attempts is reached
            elif wrong_login_count > 5:
                log = models.user.set_logger(web.ctx['ip'], data.username, data.password, dt_string, "user blocked")
                return render.login(nav, login_form, "You've entered the wrong password too many times. Account is blocked.")
            else:
                models.user.increment_wrong_login_count(userid)
                log = models.user.set_logger(web.ctx['ip'], data.username, data.password, dt_string, "Logging failed")
                return render.login(nav, login_form, "User authentication failed.")

        # If there is a matching user/password in the database the user is logged in
        elif userid and user:
            if models.user.get_wrong_login_count(userid) is None or models.user.get_wrong_login_count(userid) <= 5:
                models.user.set_wrong_login_count(userid, 0, False)  # Resets wrong pwd count
                self.login(user[1], user[0], data.remember)
                raise web.seeother("/")

            else:
                log = models.user.set_logger(web.ctx['ip'], data.username, data.password, dt_string, "account is blocked")
                print(log)
                return render.login(nav, login_form, "You've entered the wrong password too many times. Account is blocked.")
        else:
            log = models.user.set_logger(web.ctx['ip'], data.username, data.password, dt_string, "Logging failed")
            return render.login(nav, login_form, "User authentication failed.")





    def login(self, username, userid, remember):
        """
        Log in to the application
        """
        session = web.ctx.session
        session.username = username
        session.userid = userid
        if remember:
            rememberme = self.rememberme()
            web.setcookie('remember', rememberme, 2629743)

    def check_rememberme(self):
        """
        Validate the rememberme cookie and log in
        """
        username = ""
        sign = ""
        # If the user selected 'remember me' they log in automatically
        try:
            # Fetch the users cookies if it exists
            cookies = web.cookies()
            # Fetch the remember cookie and convert from string to bytes
            remember_hash = bytes(cookies.remember[2:][:-1], 'ascii')
            # Decode the hash
            decode = base64.b64decode(remember_hash).decode('utf-8')
            # Load the decoded hash to receive the host signature and the username
            username, sign = json.loads(decode)
        except AttributeError as e:
            # The user did not have the stored remember me cookie
            pass

        # If the users signed cookie matches the host signature then log in
        if self.sign_username(username) == sign:
            userid = models.user.get_user_id_by_name(username)
            self.login(username, userid, False)

    def rememberme(self):
        """
        Encode a base64 object consisting of the username signed with the
        host secret key and the username. Can be reassembled with the
        hosts secret key to validate user.
            :return: base64 object consisting of signed username and username
        """
        session = web.ctx.session
        creds = [ session.username, self.sign_username(session.username) ]
        return base64.b64encode(json.dumps(creds).encode('utf-8'))

    @classmethod
    def sign_username(self, username):
        """
        Sign the current users name with the hosts secret key
            :return: The users signed name
        """
        secret = base64.b64decode(self.secret)
        return hmac.HMAC(secret, username.encode('ascii')).hexdigest()
 