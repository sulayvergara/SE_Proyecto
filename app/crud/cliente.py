from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate


async def create_cliente(session: AsyncSession, data: ClienteCreate) -> Cliente:
    cliente = Cliente(**data.model_dump())
    session.add(cliente)
    await session.commit()
    await session.refresh(cliente)
    return cliente


async def get_cliente(session: AsyncSession, cliente_id: int) -> Cliente | None:
    result = await session.execute(
        select(Cliente).where(Cliente.id == cliente_id)
    )
    return result.scalar_one_or_none()


async def list_clientes(session: AsyncSession) -> list[Cliente]:
    result = await session.execute(select(Cliente))
    return result.scalars().all()


async def delete_cliente(session: AsyncSession, cliente_id: int) -> bool:
    cliente = await get_cliente(session, cliente_id)
    if not cliente:
        return False
    await session.delete(cliente)
    await session.commit()
    return True


async def update_cliente(session: AsyncSession, cliente_id: int, data: ClienteCreate) -> Cliente | None:
    cliente = await get_cliente(session, cliente_id)
    if not cliente:
        return None
    for field, value in data.model_dump().items():
        setattr(cliente, field, value)
    await session.commit()
    await session.refresh(cliente)
    return cliente
