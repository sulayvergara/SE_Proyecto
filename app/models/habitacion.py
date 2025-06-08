from sqlalchemy import Column, Integer, String, Numeric
from app.database import Base
from sqlalchemy.orm import relationship

class Habitacion(Base):
    __tablename__ = "habitaciones"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(10), unique=True, nullable=False)
    tipo = Column(String(50), nullable=False)
    precio_noche = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(20), default="disponible")  # 'disponible', 'ocupada', etc.

    reservas = relationship("Reserva", back_populates="habitacion")