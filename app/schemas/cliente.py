from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str
    documento_identidad: str
    correo: Optional[str] = None
    telefono: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    reservas: List[Reserva] = []

    class Config:
        orm_mode = True