from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_async_session
from app.schemas.reserva import ReservaCreate, ReservaRead
from app.crud import reserva as crud_reserva

router = APIRouter()

@router.post("/reservas/", response_model=ReservaRead, tags=["Reservas"])
async def crear_reserva(reserva: ReservaCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud_reserva.crear_reserva(db, reserva)

@router.get("/reservas/", response_model=List[ReservaRead], tags=["Reservas"])
async def listar_reservas(db: AsyncSession = Depends(get_async_session)):
    return await crud_reserva.obtener_reservas(db)

@router.put("/reservas/{reserva_id}/cancelar", response_model=ReservaRead, tags=["Reservas"])
async def cancelar_reserva(reserva_id: int, db: AsyncSession = Depends(get_async_session)):
    reserva = await crud_reserva.cancelar_reserva(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva