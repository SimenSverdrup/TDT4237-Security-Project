import os
import re

import web
import models.user
from views.utils import get_nav_bar
from views.forms import confirmation_form
import hashlib

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
        if models.user.match_user(data.username, data.temporary_pw):
            if data.new_pw1 == data.new_pw2:
                new_pw_encrypted = hashlib.md5(b'TDT4237' + data.new_pw1.encode('utf-8')).hexdigest()
                models.user.change_password(data.username, new_pw_encrypted)
                return render.confirmation(nav, confirmation_form, "Your email has been verified and password updated!")
            else:
                return render.confirmation(nav, confirmation_form, "New passwords not equal!")
        else:
            return render.confirmation(nav, confirmation_form, "Incorrect temporary password!")
