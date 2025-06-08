from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ingreso import Ingreso
from app.schemas.ingreso import IngresoCreate

async def crear_ingreso(db: AsyncSession, ingreso: IngresoCreate):
    db_ingreso = Ingreso(**ingreso.dict())
    db.add(db_ingreso)
    await db.commit()
    await db.refresh(db_ingreso)
    return db_ingreso

async def obtener_ingresos(db: AsyncSession):
    result = await db.execute(select(Ingreso))
    return result.scalars().all()

