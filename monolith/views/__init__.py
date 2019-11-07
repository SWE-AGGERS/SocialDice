from .auth import auth
from .follow import follow
from .home import home
from .stories import stories
from .users import users
from .wall import wall
from .search import search

blueprints = [home, auth, users, stories, wall, follow, search]
