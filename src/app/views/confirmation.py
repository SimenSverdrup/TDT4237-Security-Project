import os
import re

import web
import models.user
from views.utils import get_nav_bar
from views.forms import confirmation_form
import hashlib
import random


# Get html templates
render = web.template.render('templates/')


class Confirmation:

    def GET(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.confirmation(nav, confirmation_form, "")

    def POST(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input()
        confirmation = confirmation_form()
        if models.user.match_user(data.username, data.temporary_pw):
            if data.new_pw1 == data.new_pw2:
                if not confirmation.validates():
                    return render.register(nav, confirmation_form, "Must be at least 12 characters long.")

                alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                chars = []
                for i in range(5):
                    chars.append(random.choice(alphabet))
                    salt = "".join(chars)
                    new_pw_encrypted = hashlib.sha512(salt.encode('utf-8') + data.new_pw1.encode('utf-8')).hexdigest() + salt
                    models.user.change_password(data.username, new_pw_encrypted)
                return render.confirmation(nav, confirmation_form, "Your email has been verified and password updated!")

            else:
                return render.confirmation(nav, confirmation_form, "Password fields not equal!")
        else:
            return render.confirmation(nav, confirmation_form, "Incorrect username or temporary password!")
