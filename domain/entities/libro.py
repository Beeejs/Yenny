class Libro:
  def __init__(self, id, titulo, autor, editorial, precio, categoria, stock, anio):
    self.id = id
    self.titulo = titulo
    self.editorial = editorial
    self.precio = precio
    self.autor = autor
    self.categoria = categoria
    self.stock = stock
    self.anio = anio

  """ Getters """
  def get_id(self):
    return self.id
  
  def get_titulo(self):
    return self.titulo
  
  def get_autor(self):
    return self.autor
  
  def get_editorial(self):
    return self.editorial
  
  def get_precio(self):
    return self.precio
  
  def get_categoria(self):
    return self.categoria
  
  def get_stock(self):
    return self.stock
  
  def get_anio(self):
    return self.anio
  
  """ Setters """
  def set_titulo(self, titulo):
    self.titulo = titulo

  def set_autor(self, autor):
    self.autor = autor

  def set_editorial(self, editorial):
    self.editorial = editorial

  def set_precio(self, precio):
    self.precio = precio

  def set_categoria(self, categoria):
    self.categoria = categoria

  def set_stock(self, stock):
    self.stock = stock

  def set_anio(self, anio):
    self.anio = anio
  
