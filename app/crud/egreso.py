from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.egreso import Egreso
from app.schemas.egreso import EgresoCreate

async def crear_egreso(db: AsyncSession, egreso: EgresoCreate):
    db_egreso = Egreso(**egreso.dict())
    db.add(db_egreso)
    await db.commit()
    await db.refresh(db_egreso)
    return db_egreso

async def obtener_egresos(db: AsyncSession):
    result = await db.execute(select(Egreso))
    return result.scalars().all()

