from pydantic import BaseModel
from datetime import date

class IngresoBase(BaseModel):
    reserva_id: int
    monto: float
    descripcion: str = None

class IngresoCreate(IngresoBase):
    pass

class IngresoRead(IngresoBase):
    id: int
    fecha: date

    class Config:
        orm_mode = True
