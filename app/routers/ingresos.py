from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.schemas.ingreso import IngresoCreate, IngresoRead
from app.crud import ingreso as crud_ingreso
from typing import List

router = APIRouter(prefix="/ingresos", tags=["Ingresos"])

@router.post("/", response_model=IngresoRead)
async def crear_ingreso(ingreso: IngresoCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud_ingreso.crear_ingreso(db, ingreso)

@router.get("/", response_model=List[IngresoRead])
async def listar_ingresos(db: AsyncSession = Depends(get_async_session)):
    return await crud_ingreso.obtener_ingresos(db)
