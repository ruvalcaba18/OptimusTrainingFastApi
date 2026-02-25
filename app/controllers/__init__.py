"""
Controllers package.

Subdirectories:
  users/  → UserController (CRUD + foto de perfil)
  auth/   → AuthController (login)

Cuando agregues un nuevo dominio (por ejemplo deportes), crea:
  sports/ → SportsController
"""
from app.controllers.users.user_controller import user_controller, UserController
from app.controllers.auth.auth_controller import auth_controller, AuthController

__all__ = [
    "user_controller",
    "UserController",
    "auth_controller",
    "AuthController",
]
