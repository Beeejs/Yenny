class Categoria:
  def __init__(self, id, nombre, descripcion):
    self.id = id
    self.nombre = nombre
    self.descripcion = descripcion

  """ Getters """
  def get_id(self):
    return self.id
  
  def get_nombre(self):
    return self.nombre
  
  def get_descripcion(self):
    return self.descripcion
  
  """ Setters """
  def set_nombre(self, nombre):
    self.nombre = nombre

  def set_descripcion(self, descripcion):
    self.descripcion = descripcion