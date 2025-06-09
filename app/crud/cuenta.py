from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from app.models.cuenta import Cuenta
from app.schemas.cuenta import CuentaCreate, CuentaUpdate
from typing import List, Optional

async def crear_cuenta(db: AsyncSession, data: CuentaCreate) -> Cuenta:
    nueva_cuenta = Cuenta(**data.model_dump())
    db.add(nueva_cuenta)
    await db.commit()
    await db.refresh(nueva_cuenta)
    return nueva_cuenta


async def obtener_cuenta(db: AsyncSession, cuenta_id: int) -> Optional[Cuenta]:
    result = await db.execute(
        select(Cuenta).where(Cuenta.id == cuenta_id)
    )
    return result.scalar_one_or_none()


async def obtener_cuenta_por_codigo(db: AsyncSession, codigo: str) -> Optional[Cuenta]:
    result = await db.execute(
        select(Cuenta).where(Cuenta.codigo == codigo)
    )
    return result.scalar_one_or_none()

async def listar_cuentas(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Cuenta]:
    result = await db.execute(
        select(Cuenta).order_by(Cuenta.codigo).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def buscar_cuentas(db: AsyncSession, search_term: str) -> List[Cuenta]:
    search_pattern = f"%{search_term}%"
    result = await db.execute(
        select(Cuenta).where(
            or_(
                Cuenta.codigo.ilike(search_pattern),
                Cuenta.nombre.ilike(search_pattern)
            )
        ).order_by(Cuenta.codigo)
    )
    return result.scalars().all()

async def actualizar_cuenta(db: AsyncSession, cuenta_id: int, data: CuentaUpdate) -> Optional[Cuenta]:
    cuenta = await obtener_cuenta(db, cuenta_id)
    if not cuenta:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cuenta, field, value)
    
    await db.commit()
    await db.refresh(cuenta)
    return cuenta

async def eliminar_cuenta(db: AsyncSession, cuenta_id: int) -> bool:
    cuenta = await obtener_cuenta(db, cuenta_id)
    if not cuenta:
        return False
    
    await db.delete(cuenta)
    await db.commit()
    return True
