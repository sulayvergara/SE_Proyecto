from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.factura import FacturaCreate, FacturaOut
from app.crud import factura as crud_factura
from app.database import get_async_session
from typing import List

router = APIRouter(tags=["Facturas"])

@router.post("/facturas", response_model=FacturaOut)
async def crear_factura(factura: FacturaCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud_factura.crear_factura(db, factura)

@router.get("/facturas", response_model=List[FacturaOut])
async def listar_facturas(db: AsyncSession = Depends(get_async_session)):
    return await crud_factura.obtener_facturas(db)