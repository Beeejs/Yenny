from data.repositories.category_repository import CategoryRepository
from typing import Any, Dict, List, Tuple

class CategoryManager:
  def __init__(self):
    self.repo = CategoryRepository()

  def get_all(self) -> Tuple[bool, List[Dict[str, Any]], str | None]:
    try:
      categories = self.repo.get_all()
      return True, categories, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def get_one(self, category_id: int) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      category = self.repo.get_one(category_id)
      if category is None:
        return False, [], "Categoria no encontrada"
      return True, category, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def create(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      new_category_id = self.repo.create(data)
      
      if new_category_id is None:
        return False, [], "Fallo al crear la categoria en la DB."
      
      return True, data, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def update(self, category_id: int, data_update: Dict[str, Any]) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    
    try:
      updated_category = self.repo.get_one(category_id)

      if updated_category is None:
        return False, [], "Categoria a actualizar no encontrada."
      
      updated_category.update(data_update)

      self.repo.update(category_id, updated_category)
      
      return True, updated_category, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def delete(self, category_id: int) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      category_to_delete = self.repo.get_one(category_id)
      if category_to_delete is None:
        return False, [], "Categoria a eliminar no encontrada."
          
      self.repo.delete(category_id)
      
      return True, category_to_delete["id_categoria"], ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)
