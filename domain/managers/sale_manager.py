from data.repositories.sale_repository import SaleRepository
from data.repositories.user_repository import UserRepository
from data.repositories.book_repository import BookRepository
from typing import Any, Dict, List, Tuple
from pydantic import ValidationError 
from domain.validations.sale_validator import SaleCreate
from domain.validations.format_errors import format_pydantic_errors
from datetime import datetime

class SaleManager:
  def __init__(self):
    self.repo = SaleRepository()
    self.repo_user = UserRepository()
    self.repo_book = BookRepository()

  def get_all(self) -> Tuple[bool, List[Dict[str, Any]], str | None]:
    try:
      sales = self.repo.get_all()
      return True, sales, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def get_one(self, sale_id: int) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      sale = self.repo.get_one(sale_id)
      if sale is None:
        return False, [], "Venta no encontrada"
      return True, sale, ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def create(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      # Validamos datos
      payload = SaleCreate.model_validate(data).model_dump()

      date = datetime.now().isoformat(timespec="seconds")

      try:

        user = self.repo_user.get_one(None, data["id_usuario"])

        # Validaciones de logica
        if(payload["metodo_pago"] not in ["EFECTIVO", "TARJETA", "TRANSFERENCIA"]):
          return False, [], "Metodo de pago no valido"

        if(payload["estado"] not in ["CONFIRMADO", "PENDIENTE", "CANCELADA"]):
          return False, [], "Estado de venta no valido"
        
        if(len(payload["items"]) == 0):
          return False, [], "Venta sin items"
        
        # validar usuario
        if(user is None):
          return False, [], "El usuario no existe."
        
        for it in payload["items"]:
          # validar libros
          book = self.repo_book.get_one(it["id_libro"])
          if(book is None):
            return False, [], f"El libro {it['id_libro']} no existe."
        
        new_sale_id = self.repo.create({
          "id_usuario": payload["id_usuario"],
          "fecha": date,
          "metodo_pago": payload["metodo_pago"],
          "estado": payload["estado"]
        })

        self.repo.insert_detalles(
          new_sale_id,
          [
            {
              "id_libro": it["id_libro"],
              "cantidad": it["cantidad"],
              "precio_unitario": it["precio_unitario"],
              "subtotal": (it["precio_unitario"] * it["cantidad"])
            }
            for it in payload["items"]
          ]
        )

        day = date[:10]

        sale_qty = 1
        books_qty = sum(int(it["cantidad"]) for it in payload["items"])
        total = float(sum(it["precio_unitario"] * it["cantidad"] for it in payload["items"]))

        # reporte_venta_diaria
        self.repo.upsert_reporte_diario(
          payload["id_usuario"], day, sale_qty, books_qty, total
        )

        # popularidad_libro_diaria
        for it in payload["items"]:
          items_qty = int(it["cantidad"])
          income = float(it["precio_unitario"] * it["cantidad"])
          self.repo.upsert_popularidad_libro(it["id_libro"], day, items_qty, income)

        self.repo.db.commit()
      except Exception:
        self.repo.db.rollback()
        raise
      
      if new_sale_id is None:
        return False, [], "Fallo al crear la venta en la DB."
      
      return True, data, ""
      
    except ValidationError as e:
      error_messages = format_pydantic_errors(e.errors())
      return False, None, error_messages
    
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)

  def delete(self, sale_id: int) -> Tuple[bool, Dict[str, Any] | None, str | None]:
    try:
      sale_to_delete = self.repo.get_one(sale_id)
      if sale_to_delete is None:
        return False, [], "Venta no encontrada."
          
      self.repo.delete(sale_id)
      
      return True, sale_to_delete["id_venta"], ""
    except Exception as e:
      return False, [],  "Exception: Algo salio mal ->" + str(e)
