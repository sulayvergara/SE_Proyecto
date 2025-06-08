from sqlalchemy import Column, Integer, ForeignKey, Numeric, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date

class Ingreso(Base):
    __tablename__ = "ingresos"

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"))
    monto = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(Text)
    fecha = Column(Date, default=date.today)

#falta la relacion