from sqlalchemy import Column, Integer, String
from app.database import Base

class Cuenta(Base):
    __tablename__ = "cuentas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String(10), nullable=False, unique=True)  
    nombre = Column(String(100), nullable=False)  
    tipo = Column(String(20), nullable=False)     
    nivel = Column(Integer, nullable=False)