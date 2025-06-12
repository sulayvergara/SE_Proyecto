from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from .pago import PagoOut

class FacturaBase(BaseModel):
    reserva_id: int
    fecha_emision: date
    total: float
    estado: Optional[str] = "pendiente"

class FacturaCreate(FacturaBase):
    pass

class FacturaOut(FacturaBase):
    id: int
    pagos: List[PagoOut] = []

    class Config:
        orm_mode = True