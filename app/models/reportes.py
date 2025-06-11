from sqlalchemy import Column, Integer, String, Date, Numeric, Text
from app.database import Base

class VistaLibroDiario(Base):
    __tablename__ = "vistadellibro_diario"
    
    # SQLAlchemy necesita una clave primaria, usamos una combinación de campos
    # Como las vistas no tienen PK real, creamos una artificial
    fecha = Column(Date, primary_key=True)
    tipo = Column(String(20), primary_key=True)
    descripcion = Column(Text, primary_key=True)
    monto = Column(Numeric(10, 2), nullable=False)

    class Config:
        managed = False  # Indica que SQLAlchemy no debe gestionar esta tabla


class VistaRegistroHuespedes(Base):
    __tablename__ = "vistadelregistro_huespedes"
    
    cliente = Column(String(100), primary_key=True)
    documento_identidad = Column(String(20), primary_key=True)
    correo = Column(String(100))
    telefono = Column(String(20))
    fecha_inicio = Column(Date, primary_key=True)
    fecha_fin = Column(Date)
    habitacion = Column(String(10))
    tipo_habitacion = Column(String(50))
    estado_reserva = Column(String(20))

    class Config:
        managed = False


class VistaRegistroOcupacion(Base):
    __tablename__ = "vistadelregistro_ocupacion"
    
    habitacion = Column(String(10), primary_key=True)
    tipo = Column(String(50))
    fecha_inicio = Column(Date, primary_key=True)
    fecha_fin = Column(Date)
    estado_reserva = Column(String(20))
    cliente = Column(String(100))