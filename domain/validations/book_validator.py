from pydantic import BaseModel, StrictInt, StrictFloat, StrictStr, Field, condecimal, conint, ValidationError
from typing import Optional

class BookCreate(BaseModel):
  titulo: StrictStr = Field(..., min_length=1, max_length=150, description="Título del libro")
  editorial: StrictStr = Field(..., min_length=1, max_length=100, description="Editorial")
  autor: StrictStr = Field(..., min_length=1, max_length=100, description="Autor del libro")
  anio:StrictInt = Field(..., description="Año de publicación (e.g., 2024)") # que no sea negativo
  precio: StrictFloat = Field(..., description="Precio del libro, no negativo") # que no sea negativo
  stock: StrictInt = Field(..., description="Cantidad de libros en stock, no negativo") # que no sea negativo
  
  # Configuración para fallar si hay campos extra no definidos en el modelo
  class Config:
    extra = "forbid" 

class BookUpdate(BaseModel):
  titulo: Optional[StrictStr] = Field(None, min_length=1, max_length=150)
  editorial: Optional[StrictStr] = Field(None, min_length=1, max_length=100)
  autor: Optional[StrictStr] = Field(None, min_length=1, max_length=100)
  anio: Optional[conint(ge=1800, le=2100)] = Field(None)
  precio: Optional[condecimal(ge=0, decimal_places=2)] = Field(None)
  stock: Optional[conint(ge=0)] = Field(None)
  
  class Config:
    # Configuración para fallar si hay campos extra no definidos en el modelo
    extra = "forbid" 