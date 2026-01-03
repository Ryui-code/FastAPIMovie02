from .views import *
from fastapi import FastAPI
from sqladmin import Admin
from fas_movie.database.db import engine

def admin_setup(fas_movie: FastAPI):
    admin = Admin(fas_movie, engine)
    admin.add_view(CustomUserAdmin)
    admin.add_view(CustomUserRefreshTokenAdmin)
    admin.add_view(MovieAdmin)
    admin.add_view(ActorAdmin)
    admin.add_view(RatingAdmin)