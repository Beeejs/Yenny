from pydantic import BaseModel, StrictStr, Field, ConfigDict
from typing import Optional

class CategoryCreate(BaseModel):
  nombre: StrictStr = Field(..., min_length=1, max_length=100, description="Nombre de Categoría")
  descripcion: StrictStr = Field(..., max_length=250, description="Descripcion de Categoría")
  
  # Configuración para fallar si hay campos extra no definidos en el modelo
  model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True,
  )

class CategoryUpdate(BaseModel):
  nombre: Optional[StrictStr] = Field(..., min_length=1, max_length=100, description="Nombre de Categoría")
  descripcion: Optional[StrictStr]= Field(..., max_length=250, description="Descripcion de Categoría")
  
  # Configuración para fallar si hay campos extra no definidos en el modelo
  model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True,
  )