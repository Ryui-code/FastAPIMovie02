from fas_movie.database.models import *
from sqladmin import ModelView

class CustomUserAdmin(ModelView, model=CustomUser):
    column_list = [i.key for i in CustomUser.__mapper__.columns]

class CustomUserRefreshTokenAdmin(ModelView, model=CustomUserRefreshToken):
    column_list = [i.key for i in CustomUserRefreshToken.__mapper__.columns]

class MovieAdmin(ModelView, model=Movie):
    column_list = [i.key for i in Movie.__mapper__.columns]

class ActorAdmin(ModelView, model=Actor):
    column_list = [i.key for i in Actor.__mapper__.columns]

class RatingAdmin(ModelView, model=Rating):
    column_list = [i.key for i in Rating.__mapper__.columns]