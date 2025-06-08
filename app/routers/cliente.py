from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cliente import ClienteCreate, ClienteOut
from app.crud import cliente as crud_cliente
from app.database import get_async_session
from typing import List

router = APIRouter()

@router.post("/", response_model=ClienteOut, tags=["Clientes"])
async def crear_cliente(cliente: ClienteCreate, db: AsyncSession = Depends(get_async_session)):
    existente = await crud_cliente.obtener_cliente_por_documento(db, cliente.documento_identidad)
    if existente:
        raise HTTPException(status_code=400, detail="El cliente ya existe")
    return await crud_cliente.crear_cliente(db, cliente)

@router.get("/", response_model=List[ClienteOut], tags=["Clientes"])
async def listar_clientes(db: AsyncSession = Depends(get_async_session)):
    return await crud_cliente.obtener_clientes(db)

@router.get("/{cliente_id}", response_model=ClienteOut, tags=["Clientes"])
async def obtener_cliente(cliente_id: int, db: AsyncSession = Depends(get_async_session)):
    cliente = await crud_cliente.obtener_cliente_por_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente
