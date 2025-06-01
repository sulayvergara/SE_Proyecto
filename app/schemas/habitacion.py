from pydantic import BaseModel

class HabitacionBase(BaseModel):
    numero: str
    tipo: str
    precio_noche: float
    estado: str = "disponible"


class HabitacionCreate(HabitacionBase):
    pass

class HabitacionOut(HabitacionBase):
    id: int

    class Config:
        orm_mode = True
