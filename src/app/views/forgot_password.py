import os
import string

import web
from views.forms import forgot_password_form
import models.user
from views.utils import get_nav_bar
import random
from models.database import db
import mysql.connector
import re

# Get html templates
render = web.template.render('templates/')


class Forgot_password:

    def GET(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.register(nav, forgot_password_form, "")

    def POST(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input()

        try:
            smtp_server = "molde.idi.ntnu.no:25" #os.getenv("smtp server") + " :25"
            web.config.smtp_server = smtp_server
        except:
            smtp_server = "molde.idi.ntnu.no:25"
            web.config.smtp_server = smtp_server

        db.connect()
        cursor = db.cursor()
        query = ("SELECT email from users WHERE username =\"" + data.username + "\"")
        email = ''

        try:
            cursor.execute(query)
            emails = cursor.fetchall()
            if len(emails):
                email = emails[0][0]

            if email != '':
                # user exists in database
                token = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
                auth_link = 'http://localhost:8056/confirmation'
                print(token)

                models.user.change_password(data.username, token)

                web.sendmail("beelance@ntnu.no", email, "Change password",
                             "Click the link to verify your email and confirm password: " + auth_link +
                             "\nUse temporary password: " + token)
                return render.forgot_password(nav, forgot_password_form, "Email sent!")

        except mysql.connector.Error as err:
            print("Failed executing query: {}".format(err))
            cursor.fetchall()
            exit(1)
        finally:
            cursor.close()
            db.close()

        return render.forgot_password(nav, forgot_password_form, "No user with that username")
