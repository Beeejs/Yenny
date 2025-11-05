from werkzeug.security import generate_password_hash
from data.repositories.user_repository import UserRepository
from typing import Any, Dict, List, Tuple
from pydantic import ValidationError 
from domain.validations.user_validator import UserCreate, UserUpdate
from domain.validations.format_errors import format_pydantic_errors

class UserManager:
  def __init__(self):
    self.repo = UserRepository()

  def get_all(self) -> Tuple[bool, List[Dict[str, Any]], str | None]:
    try:
      categories = self.repo.get_all()
      return True, categories, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def get_one(self, id: int) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      user = self.repo.get_one(None, id)
      if user is None:
        return False, [], "Usuario no encontrado"
      
      # Eliminamos password por seguridad. Esto en el repository dejamos que devuela password porque la necesitamos para el update o auth
      user["password"] = None

      return True, user, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def create(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      # Validamos datos
      UserCreate.model_validate(data).model_dump()

      # Validamos si el usuario ya existe
      user = self.repo.get_one(data["email"], None)
      if user is not None:
        return False, [], "El usuario ya existe."

      # Generamos hash del password
      password_hash = generate_password_hash(data["password"])
      data["password"] = password_hash

      new_user_id = self.repo.create(data)
      
      if new_user_id is None:
        return False, [], "Fallo al crear el usuario en la DB."
      
      return True, { "nombre": data["nombre"], "email": data["email"], "rol": data["rol"] }, ""
    
    except ValidationError as e:
      error_messages = format_pydantic_errors(e.errors())
      return False, None, error_messages
    
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def update(self, user_id: int, data_update: Dict[str, Any]) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    
    try:
      # Validamos datos
      UserUpdate.model_validate(data_update).model_dump()

      updated_user = self.repo.get_one(None, user_id)

      if updated_user is None:
        return False, [], "Usuario no encontrado."
      
      updated_user.update(data_update)

      self.repo.update(user_id, updated_user)

      # Eliminamos password por seguridad
      updated_user["password"] = None
      
      return True, {  "id_usuario": updated_user["id_usuario"], "nombre": updated_user["nombre"], "email": updated_user["email"], "rol": updated_user["rol"]}, ""

    except ValidationError as e:
      error_messages = format_pydantic_errors(e.errors())
      return False, None, error_messages

    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def delete(self, user_id: int) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      user_to_delete = self.repo.get_one(None,user_id)
      if user_to_delete is None:
        return False, [], "Usuario no encontrado."
          
      self.repo.delete(user_id)
      
      return True, user_to_delete["id_usuario"], ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)
