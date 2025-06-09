from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models.parametro import Parametro
from app.schemas.parametro import ParametroCreate, ParametroUpdate
from typing import List, Optional

async def get_parametro(db: AsyncSession, parametro_id: int) -> Optional[Parametro]:
    """Obtener un parámetro por ID"""
    result = await db.execute(
        select(Parametro).where(Parametro.id == parametro_id)
    )
    return result.scalar_one_or_none()

async def get_parametro_by_clave(db: AsyncSession, clave: str) -> Optional[Parametro]:
    """Obtener un parámetro por clave"""
    result = await db.execute(
        select(Parametro).where(Parametro.clave == clave)
    )
    return result.scalar_one_or_none()

async def get_parametros(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Parametro]:
    """Obtener lista de parámetros con paginación"""
    result = await db.execute(
        select(Parametro).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_parametro(db: AsyncSession, parametro: ParametroCreate) -> Parametro:
    """Crear un nuevo parámetro"""
    db_parametro = Parametro(**parametro.model_dump())
    db.add(db_parametro)
    await db.commit()
    await db.refresh(db_parametro)
    return db_parametro

async def update_parametro(db: AsyncSession, parametro_id: int, parametro_data: ParametroUpdate) -> Optional[Parametro]:
    """Actualizar un parámetro existente"""
    # Verificar que existe
    parametro = await get_parametro(db, parametro_id)
    if not parametro:
        return None
    
    # Actualizar solo los campos que no son None
    update_data = parametro_data.model_dump(exclude_unset=True)
    if update_data:
        await db.execute(
            update(Parametro)
            .where(Parametro.id == parametro_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(parametro)
    
    return parametro

async def delete_parametro(db: AsyncSession, parametro_id: int) -> bool:
    """Eliminar un parámetro"""
    parametro = await get_parametro(db, parametro_id)
    if not parametro:
        return False
    
    await db.execute(
        delete(Parametro).where(Parametro.id == parametro_id)
    )
    await db.commit()
    return True
