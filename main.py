from fastapi import FastAPI
import uvicorn
from fas_movie.api import actor, movie, auth, favorite_movie, rating, users
from fas_movie.admin.setup import admin_setup
app = FastAPI()
app.include_router(auth.auth_router)
app.include_router(users.users_router)
app.include_router(movie.movie_router)
app.include_router(actor.actor_router)
app.include_router(rating.rating_router)
app.include_router(favorite_movie.favorite_movie_router)

admin_setup(app)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)