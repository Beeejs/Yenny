# domain/managers/user_manager.py
from werkzeug.security import generate_password_hash, check_password_hash
from data.repositories.user_repository import UserRepository

class AuthManager:
  def __init__(self):
    self.repo = UserRepository()

  def register(self, data: dict):
    try:
      # Generamos hash del password
      password_hash = generate_password_hash(data["password"])
      data["password"] = password_hash

      # Asignamos rol
      data["rol"] = "CLIENTE"

      # Creamos el usuario
      self.repo.create(data)
      return True, {"nombre": data["nombre"], "email": data["email"], "rol": "CLIENTE"}, ""
    except Exception as e:
      return False, {"message": "Exception: Algo salio mal", "error": str(e)}
  
  def login(self, email: str, password: str):
    try:
      user = self.repo.get_user_by_email(email)

      # Validamos si el usuario existe
      if user is None:
        return False, [], "El usuario no existe."

      # Validamos credenciales
      password_hash = user.get("password")
      if not check_password_hash(password_hash, password):
        return False, [], "Nombre de usuario o contraseña incorrectos."

      return True, {"email": user.get("email"), "nombre": user.get("nombre"), "rol": user.get("rol")}, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)
