from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(String, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    documento_identidad = Column(String(20), unique=True, nullable=False)
    correo = Column(String(100))
    telefono = Column(String(20))

    reservas = relationship("Reserva", back_populates="clientes")


