from pydantic import BaseModel, EmailStr, constr

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol_id: int

class UsuarioCreate(UsuarioBase):
    contraseña: constr(min_length=6, max_length=100)

class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

class UsuarioCorreo(UsuarioBase):
    correo: EmailStr
    
