# domain/managers/user_manager.py
from werkzeug.security import generate_password_hash
from data.repositories.user_repository import UserRepository

class AuthManager:
  def __init__(self):
    self.repo = UserRepository()

  def register(self, nombre: str, rol: str, password: str):
    # Generamos hash del password
    password_hash = generate_password_hash(password)

    # Guardamos
    user_id = self.repo.create(nombre, rol, password_hash)
    return True, {"id_usuario": user_id, "nombre": nombre, "rol": rol}
