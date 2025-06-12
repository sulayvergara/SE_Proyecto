from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.pago import PagoCreate, PagoOut
from app.crud import pago as crud_pago
from app.database import get_async_session
from typing import List

router = APIRouter(tags=["Pagos"])

@router.post("/pagos", response_model=PagoOut)
async def crear_pago(pago: PagoCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud_pago.crear_pago(db, pago)

@router.get("/pagos", response_model=List[PagoOut])
async def listar_pagos(db: AsyncSession = Depends(get_async_session)):
    return await crud_pago.obtener_pagos(db)