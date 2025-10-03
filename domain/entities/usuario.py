class Usuario:
  def __init__(self, id, nombre, rol, password):
    self.id = id
    self.nombre = nombre
    self.rol = rol
    self.password = password

  """ Getters """
  def get_id(self):
    return self.id
  
  def get_nombre(self):
    return self.nombre
  
  def get_rol(self):
    return self.rol

  def get_password(self):
    return self.password
  
  """ Setters """
  def set_nombre(self, nombre):
    self.nombre = nombre

  def set_rol(self, rol):
    self.rol = rol