from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reserva import Reserva
from app.models.habitacion import Habitacion
from app.schemas.reserva import ReservaCreate
from fastapi import HTTPException

async def crear_reserva(db: AsyncSession, reserva: ReservaCreate):
    # 1. Verificar fechas
    if reserva.fecha_inicio >= reserva.fecha_fin:
        raise HTTPException(status_code=400, detail="La fecha de inicio debe ser anterior a la fecha de fin.")

    # 2. Verificar disponibilidad de la habitación
    hab_result = await db.execute(select(Habitacion).where(Habitacion.id == reserva.habitacion_id))
    habitacion = hab_result.scalar_one_or_none()
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada.")
    if habitacion.estado != "disponible":
        raise HTTPException(status_code=400, detail="La habitación no está disponible.")

    # 3. Verificar conflictos de fechas
    result = await db.execute(
        select(Reserva).where(
            Reserva.habitacion_id == reserva.habitacion_id,
            Reserva.estado == "reservada",
            or_(
                and_(Reserva.fecha_inicio <= reserva.fecha_inicio, Reserva.fecha_fin > reserva.fecha_inicio),
                and_(Reserva.fecha_inicio < reserva.fecha_fin, Reserva.fecha_fin >= reserva.fecha_fin),
                and_(Reserva.fecha_inicio >= reserva.fecha_inicio, Reserva.fecha_fin <= reserva.fecha_fin),
            )
        )
    )
    conflictos = result.scalars().all()
    if conflictos:
        raise HTTPException(status_code=400, detail="Ya existe una reserva para esa habitación en el rango de fechas.")

    # 4. Crear reserva
    nueva_reserva = Reserva(**reserva.dict())
    db.add(nueva_reserva)
    habitacion.estado = "ocupada"
    await db.commit()
    await db.refresh(nueva_reserva)
    return nueva_reserva

async def obtener_reservas(db: AsyncSession):
    result = await db.execute(select(Reserva))
    return result.scalars().all()

async def cancelar_reserva(db: AsyncSession, reserva_id: int):
    # Obtener la reserva
    result = await db.execute(select(Reserva).where(Reserva.id == reserva_id))
    reserva = result.scalar_one_or_none()

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    if reserva.estado == "cancelada":
        raise HTTPException(status_code=400, detail="La reserva ya está cancelada")

    # Cancelar la reserva
    reserva.estado = "cancelada"
    await db.commit()

    # Verificar si hay otras reservas activas para la misma habitación
    result = await db.execute(
        select(Reserva).where(
            Reserva.habitacion_id == reserva.habitacion_id,
            Reserva.estado == "reservada"
        )
    )
    reservas_activas = result.scalars().all()

    # Si no hay más reservas activas, marcar la habitación como disponible
    if not reservas_activas:
        hab_result = await db.execute(select(Habitacion).where(Habitacion.id == reserva.habitacion_id))
        habitacion = hab_result.scalar_one_or_none()
        if habitacion:
            habitacion.estado = "disponible"
            await db.commit()

    await db.refresh(reserva)
    return reserva