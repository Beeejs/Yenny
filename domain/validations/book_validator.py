from pydantic import BaseModel, StrictInt, StrictStr, StrictFloat, Field, field_validator, ConfigDict
from typing import Optional, List

class BookCreate(BaseModel):
  titulo: StrictStr = Field(..., min_length=1, max_length=150, description="Título del libro")
  editorial: StrictStr = Field(..., min_length=1, max_length=100, description="Editorial")
  autor: StrictStr = Field(..., min_length=1, max_length=100, description="Autor del libro")
  anio: StrictInt = Field(
    ..., 
    description="Año de publicación (entre 1800 y 2100). Debe ser un entero.",
    ge=1800,
    le=2100
  )
  precio: StrictFloat = Field(
    ..., 
    gt=0,
    description="Precio del libro (float con dos decimales)"
  )
  stock: StrictInt = Field(
    ...,
    description="Cantidad de libros en stock, no negativo",
    ge=0
  ) 
  categorias: List[int] = Field(default_factory=list)

  @field_validator("categorias", mode="after")
  def uniq_and_positive(cls, v):
    if len(v) != len(set(v)):
      raise ValueError("categorias contiene duplicados.")
    if any(x <= 0 for x in v):
      raise ValueError("categorias debe tener IDs positivos.")
    return v
  
  # Configuración para fallar si hay campos extra no definidos en el modelo
  model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True,
  )

class BookUpdate(BaseModel):
  titulo: Optional[StrictStr] = Field(None, min_length=1, max_length=150)
  editorial: Optional[StrictStr] = Field(None, min_length=1, max_length=100)
  autor: Optional[StrictStr] = Field(None, min_length=1, max_length=100)
  precio: Optional[StrictFloat] = Field(None, gt=0)
  stock: Optional[StrictInt] = Field(None, ge=0)
  anio : Optional[StrictInt] = Field(None, ge=1800, le=2100)
  categorias: Optional[List[int]] = None
  
  # Configuración para fallar si hay campos extra no definidos en el modelo
  model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True,
  )