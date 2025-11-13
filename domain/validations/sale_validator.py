from pydantic import BaseModel, Field, StrictInt, ConfigDict, field_validator
from typing import List, Literal
from datetime import datetime

class SaleItem(BaseModel):
  id_libro: StrictInt = Field(..., gt=0)
  cantidad: StrictInt = Field(..., ge=1)
  
  # Configuración para fallar si hay campos extra no definidos en el modelo
  model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True,
  )

class SaleCreate(BaseModel):
  id_usuario: StrictInt = Field(..., gt=0)
  fecha: datetime = Field(..., description="Fecha y hora de la venta")  # ✅ agregado
  metodo_pago: Literal["EFECTIVO", "DEBITO", "CREDITO", "TRANSFERENCIA", "OTRO"] = "OTRO"
  estado: Literal["COMPLETADA", "PENDIENTE", "ANULADA"] = "PENDIENTE"
  items: List[SaleItem] = Field(..., min_length=1)

  @field_validator("fecha", mode="before")
  def parse_fecha(cls, v):
    """
      Acepta tanto datetime como string del tipo 'YYYY-MM-DD HH:MM:SS'
      o 'YYYY-MM-DDTHH:MM'
    """
    if isinstance(v, datetime):
      return v
    if isinstance(v, str):
      try:
        # Maneja formatos comunes
        if "T" in v:
          return datetime.strptime(v, "%Y-%m-%dT%H:%M")
        elif len(v) == 19:  # ej: 2025-11-13 16:18:00
          return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        elif len(v) == 16:  # ej: 2025-11-13 16:18
          return datetime.strptime(v, "%Y-%m-%d %H:%M")
      except ValueError:
        raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD HH:MM o YYYY-MM-DDTHH:MM")
    raise ValueError("El campo 'fecha' debe ser un string o datetime válido.")

  # Configuración para fallar si hay campos extra no definidos en el modelo
  model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True,
  )