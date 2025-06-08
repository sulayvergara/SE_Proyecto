from sqlalchemy import Column, Integer, ForeignKey, Date, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    habitacion_id = Column(Integer, ForeignKey("habitaciones.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    estado = Column(String(20), default="reservada")
    fecha_reserva = Column(TIMESTAMP, server_default=func.now())

    habitacion = relationship("Habitacion", back_populates="reservas")
    cliente = relationship("Cliente", back_populates="reservas")