
from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"))
    fecha_emision = Column(Date, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(20), default="pendiente")

    pagos = relationship("Pago", back_populates="factura")