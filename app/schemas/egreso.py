from pydantic import BaseModel
from datetime import date

class EgresoBase(BaseModel):
    descripcion: str
    monto: float

class EgresoCreate(EgresoBase):
    pass

class EgresoRead(EgresoBase):
    id: int
    fecha: date

    class Config:
        orm_mode = True
