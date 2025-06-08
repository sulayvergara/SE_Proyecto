from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.schemas.egreso import EgresoCreate, EgresoRead
from app.crud import egreso as crud_egreso
from typing import List

router = APIRouter(prefix="/egresos", tags=["Egresos"])

@router.post("/", response_model=EgresoRead)
async def crear_egreso(egreso: EgresoCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud_egreso.crear_egreso(db, egreso)

@router.get("/", response_model=List[EgresoRead])
async def listar_egresos(db: AsyncSession = Depends(get_async_session)):
    return await crud_egreso.obtener_egresos(db)
