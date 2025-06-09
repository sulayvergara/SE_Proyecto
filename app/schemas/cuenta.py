from pydantic import BaseModel, Field
from typing import Literal, Optional

class CuentaBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20, description="Codigo de la cuenta")
    nombre: str = Field(..., min_length=1, max_length=100)
    tipo: Literal["activo", "pasivo", "patrimonio", "ingreso", "gasto"]
    nivel: int = Field(..., ge=1, le=5, description="Nivel debe estar entre 1 y 5")

class CuentaCreate(CuentaBase):
    pass

class CuentaUpdate(BaseModel):
    
    codigo: Optional[str] = Field(None, min_length=1, max_length=20, description="Codigo de la cuenta")
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo: Optional[Literal["activo", "pasivo", "patrimonio", "ingreso", "gasto"]] = None
    nivel: Optional[int] = Field(None, ge=1, le=5)

class Cuenta(CuentaBase):
    id: int
    
    class Config:
        from_attributes = True