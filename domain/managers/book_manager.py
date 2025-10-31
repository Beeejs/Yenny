from data.repositories.book_repository import BookRepository
from typing import Any, Dict, List, Tuple
from pydantic import ValidationError 
from domain.validations.book_validator import BookCreate, BookUpdate

class BookManager:
  def __init__(self):
    self.repo = BookRepository()

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
      # Validamos datos
      BookCreate.model_validate(data).model_dump()

      new_book_id = self.repo.create(data)
      
      if new_book_id is None:
          return False, [], "Fallo al crear el libro en la DB."
      
      return True, data, ""
    except ValidationError as e:
      return False, None, "Datos no validos: " + str(e)
    
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def update(self, book_id: int, data_update: Dict[str, Any]) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    
    try:
      updated_book = self.repo.get_one(book_id)

      if updated_book is None:
        return False, [], "Libro a actualizar no encontrado."
      
      updated_book.update(data_update)

      self.repo.update(book_id, updated_book)
      
      return True, updated_book, ""
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
