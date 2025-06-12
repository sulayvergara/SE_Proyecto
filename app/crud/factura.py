from sqlalchemy.ext.asyncio import AsyncSession
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

async def crear_factura(db: AsyncSession, factura: FacturaCreate):
    db_factura = Factura(**factura.dict())
    db.add(db_factura)
    await db.commit()
    await db.refresh(db_factura)
    return db_factura


async def obtener_facturas(db: AsyncSession):
    result = await db.execute(
        select(Factura).options(selectinload(Factura.pagos))
    )
    return result.scalars().all()