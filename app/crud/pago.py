from sqlalchemy.ext.asyncio import AsyncSession
from app.models.pago import Pago
from app.schemas.pago import PagoCreate
from sqlalchemy.future import select

async def crear_pago(db: AsyncSession, pago: PagoCreate):
    db_pago = Pago(**pago.dict())
    db.add(db_pago)
    await db.commit()
    await db.refresh(db_pago)
    return db_pago

async def obtener_pagos(db: AsyncSession):
    result = await db.execute(select(Pago))
    return result.scalars().all()