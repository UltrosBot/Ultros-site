__author__ = 'Gareth Coles'

import requests
import yaml

from bottle import request, redirect
from rauth.service import OAuth2Service
from werkzeug.urls import url_decode

github_auth_url = "https://github.com/login/oauth/authorize"
github_token_url = "https://github.com/login/oauth/access_token"

github_scope = "user:email,repo,read:org"


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        self.config = yaml.load(open("config/github.yml", "r"))
        self.github = OAuth2Service(name="github",
                                    authorize_url=github_auth_url,
                                    access_token_url=github_token_url,
                                    client_id=
                                    self.config["oauth"]["client_id"],
                                    client_secret=
                                    self.config["oauth"]["client_secret"])

        app.route("/oauth/github", ["GET", "POST"], self.callback)
        app.route("/oauth/login", ["GET", "POST"], self.login)

    def callback(self):
        r = requests.post('https://github.com/login/oauth/access_token',
                          data={
                              'client_id':
                              self.config["oauth"]["client_id"],
                              'client_secret':
                              self.config["oauth"]["client_secret"],
                              'code': request.params["code"]
                          })

        response_data = url_decode(r.text)

        access_token = response_data['access_token']

        user_data = requests.get("https://api.github.com/user",
                                 params=dict(access_token=access_token))
        user_info = user_data.json()

        return user_info

    def login(self):
        return redirect(self.github.get_authorize_url(scope=github_scope))
