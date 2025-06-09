from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate

async def crear_usuario(db: AsyncSession, data: UsuarioCreate) -> Usuario:
    nuevo_usuario = Usuario(**data.model_dump())
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario

async def obtener_usuario(db: AsyncSession, usuario_id: int) -> Usuario | None:
    result = await db.execute(
        select(Usuario).where(Usuario.id == usuario_id)
    )
    return result.scalar_one_or_none()

async def obtener_usuario_correo(db: AsyncSession, usuario_correo: str) -> Usuario | None:
    result = await db.execute(
        select(Usuario).where(Usuario.correo == usuario_correo)
    )
    return result.scalar_one_or_none()

async def listar_usuarios(db: AsyncSession) -> list[Usuario]:
    result = await db.execute(select(Usuario))
    return result.scalars().all()

async def eliminar_usuario(db: AsyncSession, usuario_id: int) -> bool:
    usuario = await obtener_usuario(db, usuario_id)
    if not usuario:
        return False
    await db.delete(usuario)
    await db.commit()
    return True

async def actualizar_usuario(db: AsyncSession, usuario_id: int, data: UsuarioCreate) -> Usuario | None:
    usuario = await obtener_usuario(db, usuario_id)
    if not usuario:
        return None
    for field, value in data.model_dump().items():
        setattr(usuario, field, value)
    await db.commit()
    await db.refresh(usuario)
    return usuario