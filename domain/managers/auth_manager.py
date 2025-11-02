# domain/managers/user_manager.py
from werkzeug.security import generate_password_hash, check_password_hash
from data.repositories.user_repository import UserRepository
from domain.validations.auth_validator import AuthLogin, AuthRegister
from pydantic import ValidationError
from domain.validations.format_errors import format_pydantic_errors

class AuthManager:
  def __init__(self):
    self.repo = UserRepository()

  def register(self, data: dict):
    try:
      # Validamos datos
      AuthRegister.model_validate(data).model_dump()

      # Generamos hash del password
      password_hash = generate_password_hash(data["password"])
      data["password"] = password_hash

      # Asignamos rol
      data["rol"] = "CLIENTE"

      # Creamos el usuario
      self.repo.create(data)
      return True, {"nombre": data["nombre"], "email": data["email"], "rol": "CLIENTE"}, ""
    except ValidationError as e:
      error_messages = format_pydantic_errors(e.errors())
      return False, None, error_messages
    
    except Exception as e:
      return False, {"message": "Exception: Algo salio mal", "error": str(e)}
  
  def login(self, data: dict):
    try:
      # Validamos datos
      AuthLogin.model_validate(data).model_dump()
      user = self.repo.get_one(data["email"], None)

      # Validamos si el usuario existe
      if user is None:
        return False, [], "El usuario no existe."

      # Validamos credenciales
      password_hash = user.get("password")
      if not check_password_hash(password_hash, data["password"]):
        return False, [], "Nombre de usuario o contraseña incorrectos."

      return True, {"email": user.get("email"), "nombre": user.get("nombre"), "rol": user.get("rol")}, ""
    except ValidationError as e:
      error_messages = format_pydantic_errors(e.errors())
      return False, None, error_messages
    
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)
