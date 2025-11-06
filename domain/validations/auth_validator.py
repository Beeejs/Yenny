from pydantic import BaseModel, StrictStr, EmailStr, Field, ConfigDict

class AuthRegister(BaseModel):
  nombre: StrictStr = Field(..., min_length=3, max_length=20, description="Nombre de usuario")
  email: EmailStr = Field(..., min_length=8, max_length=40, description="Email de usuario")
  password: StrictStr = Field(..., min_length=6, max_length=50, description="Password de usuario")
  
  # Configuración para fallar si hay campos extra no definidos en el modelo
  model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True,
  )

class AuthLogin(BaseModel):
  email: EmailStr = Field(..., min_length=8, max_length=40, description="Email de usuario")
  password: StrictStr = Field(..., min_length=6, max_length=50, description="Password de usuario")
  
  model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True,
  )