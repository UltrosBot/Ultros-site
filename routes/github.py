__author__ = 'Gareth Coles'
#
# import copy
# import requests
# import yaml
#
# from bottle import request, redirect, route
# from kitchen.text.converters import to_bytes
# from rauth.service import OAuth2Service
# from werkzeug.urls import url_decode
#
# from internal.schemas import User
#
# github_auth_url = "https://github.com/login/oauth/authorize"
# github_token_url = "https://github.com/login/oauth/access_token"
#
# github_scope = "user:email,repo,read:org"


class Routes(object):

    def __init__(self, app, manager):
        """
        :type manager internal.manager.Manager
        """

        self.app = app
        self.manager = manager
#
#         self.config = yaml.load(open("config/github.yml", "r"))
#         self.github = OAuth2Service(
#             name="github",
#             authorize_url=github_auth_url,
#             access_token_url=github_token_url,
#             client_id=self.config["oauth"]["client_id"],
#             client_secret=self.config["oauth"]["client_secret"]
#         )
#
#         route("/oauth/github", ["GET", "POST"], self.callback)
#         route("/oauth/login", ["GET", "POST"], self.login)
#
#     def callback(self):
#         session = request.environ.get("beaker.session")
#
#         r = requests.post(
#             'https://github.com/login/oauth/access_token',
#             data={
#                 'client_id': self.config["oauth"]["client_id"],
#                 'client_secret': self.config["oauth"]["client_secret"],
#                 'code': request.params["code"]
#             }
#         )
#
#         response_data = url_decode(r.text)
#
#         access_token = response_data['access_token']
#
#         data = self.get_user_data(access_token)
#
#         username = data["user"]["login"]
#         session["username"] = username
#         session.save()
#
#         return data
#
#     def login(self):
#         return redirect(self.github.get_authorize_url(scope=github_scope))
#
#     def get_user_data(self, access_token):
#         # I do not like this function.
#         # There's got to be many, much better ways to do this. :U
#         done = {}
#
#         user = requests.get("https://api.github.com/user",
#                             params=dict(access_token=access_token))
#         user = user.json()
#
#         repos_url = user["repos_url"]
#         repos = requests.get(
#             repos_url, params=dict(access_token=access_token)
#         )
#         repos = repos.json()
#
#         orgs_url = user["organizations_url"]
#         orgs = requests.get(
#             orgs_url, params=dict(access_token=access_token)
#         )
#         orgs = orgs.json()
#
#         org_repos = {}
#
#         for org in orgs:
#             url = org["repos_url"]
#             o_repos = requests.get(
#                 url, params=dict(access_token=access_token)
#             )
#             o_repos = o_repos.json()
#
#             org_repos[org["login"]] = o_repos
#
#         done["user"] = user
#         done["repos"] = repos
#         done["orgs"] = orgs
#         done["org_repos"] = org_repos
#
        # We need to sanitize a bit so that we can fit everything into the DB.
#         # TODO: Rewrite this and the schemas for better efficiency
#         # TODO: Make the below a recursive function
#
#         for key in done.keys():
#             # For each key above:
#             if isinstance(done[key], list):
#                 # If the value is a list:
#                 complete = []
#                 for l in done[key]:
#                     # For each entry in the list:
#                     for k in copy.copy(l.keys()):
#                         # For each key in the entry:
#                         if isinstance(l[k], list):
#                             # If the value is a list:
#                             _complete = []
#                             for _l in done[key][k]:
#                                 # For each entry in the list:
#                                 for _k in copy.copy(_l.keys()):
#                                     # For each key in the entry:
#                                     if _k.endswith("_url"):
#                                         # If the key ends with _url:
#                                         del _l[_k]
#                                         # Delete the entry
#                                 _complete.append(l)
#                             l[k] = _complete
#                             # Store the modified list
#                             continue
#                         elif isinstance(l[k], dict):
#                             # If the value is a dict:
#                             for _k in copy.copy(l[k].keys()):
#                                 # For each key in the dict:
#                                 if _k.endswith("_url"):
#                                     # If the key ends with _url:
#                                     del l[k][_k]
#                                     # Delete the entry
#                         if k.endswith("_url"):
#                             # If the key ends with _url:
#                             del l[k]
#                             # Delete the entry
#                     complete.append(l)
#                 done[key] = complete
#                 # Store the modified list
#                 continue
#
#             # The below is much the same as the above.
#             for k in copy.copy(done[key].keys()):
#                 if isinstance(done[key][k], list):
#                     complete = []
#                     for l in done[key][k]:
#                         for _k in copy.copy(l.keys()):
#                             if isinstance(l[_k], dict):
#                                 for __k in copy.copy(l[_k].keys()):
#                                     if __k.endswith("_url"):
#                                         del l[_k][__k]
#                             if _k.endswith("_url"):
#                                 del l[_k]
#                         complete.append(l)
#                     done[key][k] = complete
#                     continue
#                 elif isinstance(done[key][k], dict):
#                     for _k in copy.copy(done[key][k].keys()):
#                         if _k.endswith("_url"):
#                             del done[key][k][_k]
#                 if k.endswith("_url"):
#                     del done[key][k]
#
#         username = user["login"]
#
#         db = self.manager.get_session()
#
#         with db.no_autoflush:
#             # These queries can take a while so don't flush automatically.
#             user = db.query(User).filter_by(username=username).first()
#
#             if not user:
#                 # Insert user
#                 user = User(
#                     to_bytes(username), to_bytes(access_token), done["user"],
#                     done["repos"], done["orgs"], done["org_repos"]
#                 )
#                 db.add(user)
#             else:
#                 # Create user
#                 user.token = to_bytes(access_token)
#                 user.data_user = done["user"]
#                 user.data_user_repos = done["repos"]
#                 user.data_orgs = done["orgs"]
#                 user.data_orgs_repos = done["org_repos"]
#                 db.merge(user)
#
#         # Commit and close the connection to the DB
#         db.commit()
#         db.close()
#
#         return done
