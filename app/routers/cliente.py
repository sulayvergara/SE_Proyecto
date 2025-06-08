from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Cliente
from schemas import Cliente, ClienteCreate
from typing import List

router = APIRouter()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear cliente
@router.post("/", response_model=Cliente)
def crear_cliente(cliente: clienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(cliente).filter(cliente.documento_identidad == cliente.documento_identidad).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El cliente ya existe")
    nuevo_cliente = cliente(**cliente.dict())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

# Obtener todos los clientes
@router.get("/", response_model=List[cliente])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(cliente).all()

# Obtener un cliente por ID
@router.get("/{cliente_id}", response_model=cliente)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(cliente).filter(cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente