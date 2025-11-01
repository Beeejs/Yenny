from data.repositories.book_repository import BookRepository
from data.repositories.category_repository import CategoryRepository
from typing import Any, Dict, List, Tuple
from pydantic import ValidationError 
from domain.validations.book_validator import BookCreate, BookUpdate
from domain.validations.format_errors import format_pydantic_errors

class BookManager:
  def __init__(self):
    self.repo = BookRepository()
    self.category_repo = CategoryRepository()

  def get_all(self) -> Tuple[bool, List[Dict[str, Any]], str | None]:
    try:
      books = self.repo.get_all()
      return True, books, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def get_one(self, book_id: int) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      book = self.repo.get_one(book_id)
      if book is None:
        return False, [], "Libro no encontrado"
      return True, book, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def create(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      # Validamos datos. Utilizamos payload por le decimal
      payload = BookCreate.model_validate(data).model_dump()
      cat_ids = payload.get("categorias", [])
      
      # Hacer todo en una transacción, con un solo commit al final
      try:
        new_book_id = self.repo.create(payload)

        if new_book_id is None:
          return False, [], "Fallo al crear el libro en la DB."

        self.repo.set_categories(new_book_id, cat_ids)
        self.repo.db.commit() 
      except Exception:
          self.repo.db.rollback()
          raise
      
      return True, payload, ""
    except ValidationError as e:
      error_messages = format_pydantic_errors(e.errors())
      return False, None, error_messages
    
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def update(self, book_id: int, data_update: Dict[str, Any]) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    
    try:
      # Validamos datos. Utilizamos payload por le decimal
      payload = BookUpdate.model_validate(data_update).model_dump(
        exclude_unset=True,
        exclude_none=True
      )

      updated_book = self.repo.get_one(book_id)

      if updated_book is None:
        return False, [], "Libro a actualizar no encontrado."
      
      # Si vienen categorías, validar existencia antes
      if "categorias" in payload and payload["categorias"] is not None:
        ok, missing = self.category_repo.categories_exist(payload["categorias"])
        if not ok:
          return False, None, f"Categorías inexistentes: {missing}"
      
      # Actualizar libro
      updated_book.update(data_update)

      # Actualizar libro y (si hay) categorías
      try:
        self.repo.update(book_id, updated_book)  # NO hace commit
        if "categorias" in payload and payload["categorias"] is not None:
          self.repo.set_categories(book_id, payload["categorias"]) 
        self.repo.db.commit()
      except Exception:
        self.repo.db.rollback()
        raise

      
      return True, updated_book, ""
    except ValidationError as e:
      error_messages = format_pydantic_errors(e.errors())
      return False, None, error_messages
    
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def delete(self, book_id: int) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      book_to_delete = self.repo.get_one(book_id)
      if book_to_delete is None:
        return False, [], "Libro a eliminar no encontrado."
          
      self.repo.delete(book_id)
      
      return True, book_to_delete["id_libro"], ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)
