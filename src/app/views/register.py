import os

import web
from views.forms import register_form
import models.register
import models.user
from views.utils import get_nav_bar
import hashlib
import random
import string
import re

# Get html templates
render = web.template.render('templates/')


class Register:

    def GET(self):
        """
        Get the registration form

            :return: A page with the registration form
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.register(nav, register_form, "")

    def POST(self):
        """
        Handle input data and register new user in database

            :return: Main page
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input()

        register = register_form()
        if not register.validates():
            return render.register(nav, register, "All fields must be valid.")

        # Check if user exists
        if models.user.get_user_id_by_name(data.username):
            return render.register(nav, register, "Invalid user, already exists.")
        try:
            smtp_server = "molde.idi.ntnu.no:25" #os.getenv("smtp server") + " :25"
            web.config.smtp_server = smtp_server

        except:
            smtp_server = "molde.idi.ntnu.no:25"
            web.config.smtp_server = smtp_server

        #models.register.set_user(data.username,
        #                         hashlib.md5(b'TDT4237' + data.password.encode('utf-8')).hexdigest(),
        #                         data.full_name, data.company, data.email, data.street_address,
        #                         data.city, data.state, data.postal_code, data.country)

        token = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
        auth_link = 'http://localhost:8056/confirmation'

        web.sendmail("beelance@ntnu.no", data.email, "Email verification/password reset",
                     "Click the link to verify your email and confirm password: " + auth_link +
                     "\nUse temporary password: " + token)

        models.register.set_user(data.username, token,
                                data.full_name, data.company, data.email, data.street_address,
                                data.city, data.state, data.postal_code, data.country)
        print("token: " + token)

        return render.register(nav, register_form, "User registered! Check your email to complete your registration. "
                                                   "You will not be able to login until you validate your email. "
                                                   "\nIf no email is received, go to /confirmation and authenticate "
                                                   "with the token printed in the terminal.")
