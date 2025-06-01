from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.habitacion import HabitacionCreate, HabitacionOut
from app.crud import habitacion as crud_habitacion
from app.database import get_async_session

from typing import List

router = APIRouter()

@router.post("/habitaciones/", response_model=HabitacionOut)
async def crear_habitacion(habitacion: HabitacionCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud_habitacion.crear_habitacion(db, habitacion)

@router.get("/habitaciones/", response_model=List[HabitacionOut])
async def listar_habitaciones(db: AsyncSession = Depends(get_async_session)):
    return await crud_habitacion.obtener_habitaciones(db)

@router.get("/habitaciones/{habitacion_id}", response_model=HabitacionOut)
async def obtener_habitacion(habitacion_id: int, db: AsyncSession = Depends(get_async_session)):
    habitacion = await crud_habitacion.obtener_habitacion_por_id(db, habitacion_id)
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return habitacion

@router.put("/habitaciones/{habitacion_id}/estado", response_model=HabitacionOut)
async def actualizar_estado(habitacion_id: int, nuevo_estado: str, db: AsyncSession = Depends(get_async_session)):
    habitacion = await crud_habitacion.actualizar_estado_habitacion(db, habitacion_id, nuevo_estado)
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return habitacion
