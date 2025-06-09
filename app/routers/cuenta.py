from fastapi import APIRouter, Depends, HTTPException, Query,Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cuenta import CuentaCreate, CuentaUpdate, Cuenta
from app.crud import cuenta as crud_cuenta
from app.database import get_async_session
from typing import List, Optional, Literal
from sqlalchemy import func, select

router = APIRouter(tags=["Cuentas"])

@router.post("/cuentas/", response_model=Cuenta, tags=["Cuentas"])
async def crear_cuenta(cuenta: CuentaCreate, db: AsyncSession = Depends(get_async_session)):
    """Crear una nueva cuenta"""
    # Verificar que no exista una cuenta con el mismo código
    existente = await crud_cuenta.obtener_cuenta_por_codigo(db, cuenta.codigo)
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese código")
    
    return await crud_cuenta.crear_cuenta(db, cuenta)

@router.get("/cuentas/{cuenta_id}", response_model=Cuenta, tags=["Cuentas"])
async def obtener_cuenta(cuenta_id: int, db: AsyncSession = Depends(get_async_session)):
    """Obtener una cuenta específica por ID"""
    cuenta = await crud_cuenta.obtener_cuenta(db, cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return cuenta

@router.get("/cuentas/", response_model=List[Cuenta], tags=["Cuentas"])
async def listar_cuentas(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a devolver"),
    db: AsyncSession = Depends(get_async_session)
):
    """Listar todas las cuentas con paginación"""
    return await crud_cuenta.listar_cuentas(db, skip=skip, limit=limit)


@router.get("/cuentas/buscar/", response_model=List[Cuenta], tags=["Cuentas"])
async def buscar_cuentas(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    db: AsyncSession = Depends(get_async_session)
):
    """Buscar cuentas por código o nombre"""
    return await crud_cuenta.buscar_cuentas(db, q)



@router.get("/cuentas/codigo/{codigo}", response_model=Cuenta, tags=["Cuentas"])
async def obtener_cuenta_por_codigo(codigo: str, db: AsyncSession = Depends(get_async_session)):
    """Obtener una cuenta específica por código"""
    cuenta = await crud_cuenta.obtener_cuenta_por_codigo(db, codigo)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return cuenta

@router.put("/cuentas/{cuenta_id}", response_model=Cuenta, tags=["Cuentas"])
async def actualizar_cuenta(
    cuenta_id: int, 
    datos: CuentaUpdate, 
    db: AsyncSession = Depends(get_async_session)
):
    """Actualizar una cuenta existente"""
    # Si se está actualizando el código, verificar que no exista otra cuenta con ese código
    if datos.codigo:
        existente = await crud_cuenta.obtener_cuenta_por_codigo(db, datos.codigo)
        if existente and existente.id != cuenta_id:
            raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese código")
    
    actualizada = await crud_cuenta.actualizar_cuenta(db, cuenta_id, datos)
    if not actualizada:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return actualizada

@router.delete("/cuentas/{cuenta_id}", tags=["Cuentas"])
async def eliminar_cuenta(cuenta_id: int, db: AsyncSession = Depends(get_async_session)):
    """Eliminar una cuenta"""
    eliminada = await crud_cuenta.eliminar_cuenta(db, cuenta_id)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return {"mensaje": "Cuenta eliminada correctamente"}

