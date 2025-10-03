class Venta:
  def __init__(self, id, fecha, estado, metodo_pago):
    self.id = id
    self.fecha = fecha
    self.metodo_pago = metodo_pago
    self.estado = estado

  """ Getters """
  def get_id(self):
    return self.id
  
  def get_fecha(self):
    return self.fecha
  
  def get_metodo_pago(self):
    return self.metodo_pago
  
  def get_estado(self):
    return self.estado
  
  """ Setters """
  def set_fecha(self, fecha):
    self.fecha = fecha

  def set_metodo_pago(self, metodo_pago):
    self.metodo_pago = metodo_pago

  def set_estado(self, estado):
    self.estado = estado