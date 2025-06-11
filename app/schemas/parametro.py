from pydantic import BaseModel, Field
from typing import Optional

class ParametroBase(BaseModel):
    clave: str = Field(..., min_length=1, max_length=50, description="Clave única del parámetro")
    valor: str = Field(..., min_length=1, description="Valor del parámetro")
    descripcion: Optional[str] = Field(None, description="Descripción opcional del parámetro")

class ParametroCreate(ParametroBase):
    pass

class ParametroUpdate(BaseModel):
    clave: Optional[str] = Field(None, min_length=1, max_length=50)
    valor: Optional[str] = Field(None, min_length=1)
    descripcion: Optional[str] = None


class Parametro(ParametroBase):
    id: int
    
    class Config:
        from_attributes = True
