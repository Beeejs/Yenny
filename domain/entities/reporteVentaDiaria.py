class ReporteVentaDiaria:
  def __init__(self, id, dia, total_ventas, unidades, monto):
    self.id = id
    self.dia = dia
    self.total_ventas = total_ventas
    self.unidades = unidades
    self.monto = monto

  """ Getters """
  def get_id(self):
    return self.id
  
  def get_dia(self):
    return self.dia
  
  def get_total_ventas(self):
    return self.total_ventas
  
  def get_unidades(self):
    return self.unidades
  
  def get_monto(self):
    return self.monto
  
  """ Setters """
  def set_dia(self, dia):
    self.dia = dia

  def set_total_ventas(self, total_ventas):
    self.total_ventas = total_ventas

  def set_unidades(self, unidades):
    self.unidades = unidades

  def set_monto(self, monto):
    self.monto = monto