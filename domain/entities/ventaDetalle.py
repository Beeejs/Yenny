class VentaDetalle:
  def __init__(self, id, venta, libro, cantidad, precio_unitario, subtotal):
    self.id = id
    self.venta = venta
    self.libro = libro
    self.cantidad = cantidad
    self.precio_unitario = precio_unitario
    self.subtotal = subtotal

  """ Getters """
  def get_id(self):
    return self.id
  
  def get_venta(self):
    return self.venta
  
  def get_libro(self):
    return self.libro
  
  def get_cantidad(self):
    return self.cantidad
  
  def get_precio_unitario(self):
    return self.precio_unitario
  
  def get_subtotal(self):
    return self.subtotal
  
  """ Setters """
  def set_venta(self, venta):
    self.venta = venta

  def set_libro(self, libro):
    self.libro = libro

  def set_cantidad(self, cantidad):
    self.cantidad = cantidad

  def set_precio_unitario(self, precio_unitario):
    self.precio_unitario = precio_unitario

  def set_subtotal(self, subtotal):
    self.subtotal = subtotal