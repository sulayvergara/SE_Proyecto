from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.habitacion import Habitacion
from app.schemas.habitacion import HabitacionCreate

async def crear_habitacion(db: AsyncSession, habitacion: HabitacionCreate):
    db_hab = Habitacion(**habitacion.dict())
    db.add(db_hab)
    await db.commit()
    await db.refresh(db_hab)
    return db_hab

async def obtener_habitaciones(db: AsyncSession):
    result = await db.execute(select(Habitacion))
    return result.scalars().all()


async def obtener_habitacion_por_id(db: AsyncSession, habitacion_id: int):
    result = await db.execute(select(Habitacion).where(Habitacion.id == habitacion_id))
    return result.scalar_one_or_none()

async def actualizar_estado_habitacion(db: AsyncSession, habitacion_id: int, nuevo_estado: str):
    result = await db.execute(select(Habitacion).where(Habitacion.id == habitacion_id))
    habitacion = result.scalar_one_or_none()
    if habitacion:
        habitacion.estado = nuevo_estado
        await db.commit()
        await db.refresh(habitacion)
    return habitacion

