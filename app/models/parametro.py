from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Parametro(Base):
    __tablename__ = "parametros"
    
    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(50), unique=True, index=True, nullable=False)
    valor = Column(Text, nullable=False)
    descripcion = Column(Text, nullable=True)