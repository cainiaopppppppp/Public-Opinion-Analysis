# /APP/urls.py
from .extends import api
from .apis.apis import *

api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(Register, "/register")

api.add_resource(Forget, "/forget")
