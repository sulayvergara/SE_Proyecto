from pydantic import BaseModel
from datetime import date

class PagoBase(BaseModel):
    factura_id: int
    fecha_pago: date
    monto: float
    metodo_pago: str

class PagoCreate(PagoBase):
    pass

class PagoOut(PagoBase):
    id: int

    class Config:
       orm_mode = True