from pydantic import BaseModel, StrictInt, StrictStr, Field, condecimal, conint, ValidationError
from typing import Optional, List, Any, Dict

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
  precio: condecimal(ge=0, decimal_places=2) = Field(..., description="Precio del libro, no negativo y con 2 decimales de precisión") 
  stock: StrictInt = Field(
    ...,
    description="Cantidad de libros en stock, no negativo",
    ge=0
  ) 
  
  # Configuración para fallar si hay campos extra no definidos en el modelo
  class Config:
    extra = "forbid" 

class BookUpdate(BaseModel):
  titulo: Optional[StrictStr] = Field(None, min_length=1, max_length=150)
  editorial: Optional[StrictStr] = Field(None, min_length=1, max_length=100)
  autor: Optional[StrictStr] = Field(None, min_length=1, max_length=100)
  precio: Optional[condecimal(ge=0, decimal_places=2)] = Field(None)
  anio: Optional[conint(ge=1800, le=2100)] = Field(None)
  precio: Optional[condecimal(ge=0, decimal_places=2)] = Field(None)
  stock: Optional[conint(ge=0)] = Field(None)
  
  class Config:
    # Configuración para fallar si hay campos extra no definidos en el modelo
    extra = "forbid"


# funcion para hacer que los mensajes de errores sean legibles
def format_pydantic_errors(errors: List[Dict[str, Any]]) -> List[str]:
  formatted_messages = []
  
  # Diccionario de errores comunes para hacer la traducción/limpieza
  error_map = {
    'extra_forbidden': 'no está permitido. Elimine este campo.',
    'string_type': 'debe ser una cadena de texto (string).',
    'int_type': 'debe ser un número entero (integer).',
    'decimal_type': 'debe ser un número.',
    'value_error': 'no cumple con la restricción de valor (revisar rango o decimales).',
    'too_long': 'es demasiado largo.',
    'too_short': 'es demasiado corto.'
  }
  
  for error in errors:
    loc = error['loc'] # Tupla con la ubicación del error, ej: ('anio',)
    msg = error['msg']
    type_error = error['type'] # El código del error de Pydantic, ej: 'extra_forbidden'

    # Determinar el nombre del campo. Si loc tiene más de un elemento, tomamos el primero.
    field_name = str(loc[0]) if loc else "Datos"

    # Intentar crear un mensaje limpio
    clean_msg = f"El campo '{field_name}' "
    
    if type_error == 'extra_forbidden':
        # Manejo especial para campos extra no permitidos
        clean_msg = f"Existen claves no permitidas." 
    elif type_error in error_map:
        # Usar la traducción simple
        clean_msg += error_map[type_error]
    elif 'must be a value' in msg:
        # Manejar errores de rango (ge/le)
          clean_msg += f"debe estar dentro del rango permitido. {msg.split('value ')[1]}"
    else:
        # Si no se puede traducir, devolver el mensaje original de Pydantic
        clean_msg += f"falló la validación: {msg}"

    formatted_messages.append(clean_msg)
      
  return formatted_messages