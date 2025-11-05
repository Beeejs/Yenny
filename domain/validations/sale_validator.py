from pydantic import BaseModel, Field, StrictInt, StrictStr, field_validator
from typing import List, Literal
from decimal import Decimal, ROUND_HALF_UP

class SaleItem(BaseModel):
  id_libro: StrictInt = Field(..., gt=0)
  cantidad: StrictInt = Field(..., ge=1)
  precio_unitario: Decimal = Field(..., gt=0)

  @field_validator("precio_unitario", mode="after")
  def dos_decimales(cls, v):
    if -v.as_tuple().exponent > 2:
      raise ValueError("El precio no puede tener más de 2 decimales.")
    return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
  
  # Configuración para fallar si hay campos extra no definidos en el modelo
  class Config:
    extra = "forbid" 

class SaleCreate(BaseModel):
  id_usuario: StrictInt = Field(..., gt=0)
  metodo_pago: Literal["EFECTIVO", "DEBITO", "CREDITO", "TRANSFERENCIA", "OTRO"] = "OTRO"
  estado: Literal["COMPLETADA", "PENDIENTE", "ANULADA"] = "PENDIENTE"
  items: List[SaleItem] = Field(..., min_length=1)

  # Configuración para fallar si hay campos extra no definidos en el modelo
  class Config:
    extra = "forbid" 