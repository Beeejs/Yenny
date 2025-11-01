from pydantic import BaseModel, StrictStr, EmailStr, Field

class AuthRegister(BaseModel):
  nombre: StrictStr = Field(..., min_length=3, max_length=20, description="Nombre de usuario")
  email: EmailStr = Field(..., min_length=8, max_length=40, description="Email de usuario")
  password: StrictStr = Field(..., min_length=6, max_length=20, description="Password de usuario")
  
  # Configuración para fallar si hay campos extra no definidos en el modelo
  class Config:
    extra = "forbid" 

class AuthLogin(BaseModel):
  email: EmailStr = Field(..., min_length=8, max_length=40, description="Email de usuario")
  password: StrictStr = Field(..., min_length=6, max_length=20, description="Password de usuario")
  
  class Config:
    # Configuración para fallar si hay campos extra no definidos en el modelo
    extra = "forbid"