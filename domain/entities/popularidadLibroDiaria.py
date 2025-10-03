class PopularidadLibroDiaria:
    def __init__(self, id, libro, dia, unidades, ingresos):
        self.id = id
        self.libro = libro
        self.dia = dia
        self.unidades = unidades
        self.ingresos = ingresos

    """ Getters """
    def get_libro(self):
        return self.libro
    
    def get_dia(self):
        return self.dia
    
    def get_unidades(self):
        return self.unidades
    
    def get_ingresos(self):
        return self.ingresos
    
    """ Setters """
    def set_libro(self, libro):
        self.libro = libro

    def set_dia(self, dia):
        self.dia = dia

    def set_unidades(self, unidades):
        self.unidades = unidades

    def set_ingresos(self, ingresos):
        self.ingresos = ingresos