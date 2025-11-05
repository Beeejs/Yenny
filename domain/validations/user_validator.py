# domain/validations/user_validator.py
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field, StrictStr, field_validator

class UserCreate(BaseModel):
  nombre: StrictStr = Field(..., min_length=3, max_length=20, description="Nombre de usuario")
  email: EmailStr = Field(..., min_length=8, max_length=40, description="Email de usuario")
  password: StrictStr = Field(..., min_length=6, max_length=50, description="Password en texto plano (se hashea luego)")
  rol: Literal["ADMIN", "GERENTE", "EMPLEADO"] = "EMPLEADO"

  # --- normalizaciones/limpieza ---
  @field_validator("nombre")
  @classmethod
  def _strip_nombre(cls, v: str) -> str:
    return v.strip()

  # Configuración para fallar si hay campos extra no definidos en el modelo
  class Config:
    extra = "forbid"


class UserUpdate(BaseModel):
  nombre: Optional[StrictStr] = Field(..., min_length=3, max_length=20, description="Nombre de usuario")
  email: Optional[EmailStr] = Field(..., min_length=8, max_length=40, description="Email de usuario")
  rol: Optional[Literal["ADMIN", "GERENTE", "EMPLEADO"]] = None

  @field_validator("nombre")
  @classmethod
  def _strip_nombre(cls, v: Optional[str]) -> Optional[str]:
    return v.strip() if v is not None else v

  # Configuración para fallar si hay campos extra no definidos en el modelo
  class Config:
    extra = "forbid"