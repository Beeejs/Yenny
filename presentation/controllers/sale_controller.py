# presentation/controllers/sell_controller.py
from flask import jsonify
from domain.managers.sale_manager import SaleManager

# TODO: VALIDAR QUE NO VENGAN CAMPOS NO PERMITIDOS (ver si se puede llegar a implementar)
def get_all():
  sell_manager = SaleManager()
  
  # Obtener ventas
  ok, sales, message = sell_manager.get_all()

  if not ok:
    return jsonify(
      {
        "status": False,
        "message": message or "Algo salio mal",
      }
    ), 400

  return jsonify(
    {
      "status": True,
      "message": "Ventas obtenidas correctamente",
      "response": sales
    }
  ), 200


def get_one(id: int):
  sale_manager = SaleManager()
  
  # Obtener venta
  ok, sale, message = sale_manager.get_one(id)

  if not ok:
    return jsonify(
      {
        "status": False,
        "message": message or  "Algo salio mal",
      }
    ), 400

  return jsonify(
    {
      "status": True,
      "message": "Venta obtenida correctamente",
      "response": sale
    }
  ), 200

def create(data: dict):
  sale_manager = SaleManager()
  
  # Crear venta
  ok, sale, message = sale_manager.create(data)
  
  if not ok:
    return jsonify(
      {
        "status": False,
        "message": message or "Algo salio mal",
      }
    ), 400

  return jsonify(
    {
      "status": True,
      "message": "Venta creada correctamente",
      "response": sale
    }
  ), 200


def update(id: int, data_update: dict):
  sale_manager = SaleManager()
  
  # Actualizar venta
  ok, sale, message = sale_manager.update(id, data_update)

  if not ok:
    return jsonify(
      {
        "status": False,
        "message": message or  "Algo salio mal",
      }
    ), 400

  return jsonify(
    {
      "status": True,
      "message": "Venta actualizada correctamente",
      "response": sale
    }
  ), 200


def delete(id: int):
  sale_manager = SaleManager()
  
  # Eliminar venta
  ok, sale, message = sale_manager.delete(id)

  if not ok:
    return jsonify(
      {
        "status": False,
        "message": message or "Algo salio mal",
      }
    ), 400

  return jsonify(
    {
      "status": True,
      "message": "Venta eliminada correctamente"
    }
  ), 200
  
