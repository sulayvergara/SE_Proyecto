from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cliente import ClienteCreate, Cliente
from app.crud import cliente as crud_cliente
from app.database import get_async_session
from typing import List

router = APIRouter()

@router.post("/clientes/", response_model=ClienteCreate, tags=["Clientes"])
async def create_cliente(cliente: ClienteCreate, db: AsyncSession = Depends(get_async_session)):
    existente = await crud_cliente.get_cliente(db, cliente.documento_identidad)
    if existente:
        raise HTTPException(status_code=400, detail="El cliente ya existe")
    return await crud_cliente.create_cliente(db, cliente)

@router.get("/clientes/", response_model=List[Cliente], tags=["Clientes"])
async def listar_clientes(db: AsyncSession = Depends(get_async_session)):
    return await crud_cliente.list_clientes(db)

@router.get("/clientes/{cliente_id}", response_model=Cliente, tags=["Clientes"])
async def create_cliente(cliente_id: int, db: AsyncSession = Depends(get_async_session)):
    cliente = await crud_cliente.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente