import os
import re

import web
from models.database import db
import mysql.connector
import models.user
from views.utils import get_nav_bar
import hashlib

# Get html templates
render = web.template.render('templates/')


class Confirmation:
    id = ''

    def GET(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        self.id = web.input().id
        return render.register(nav, "Your email has been verified!")

    def POST(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.register(nav, "Your email has been verified!")
