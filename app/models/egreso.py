from sqlalchemy import Column, Integer, Text, Numeric, Date
from app.database import Base
from datetime import date

class Egreso(Base):
    __tablename__ = "egresos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    fecha = Column(Date, default=date.today)
