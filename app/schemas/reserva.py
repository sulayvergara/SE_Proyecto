from pydantic import BaseModel
from datetime import date, datetime

class ReservaBase(BaseModel):
    cliente_id: int
    habitacion_id: int
    fecha_inicio: date
    fecha_fin: date

class ReservaCreate(ReservaBase):
    pass

class ReservaRead(ReservaBase):
    id: int
    estado: str
    fecha_reserva: datetime

    class Config:
        orm_mode = True