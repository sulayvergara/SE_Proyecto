from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_async_session
from app.schemas.parametro import Parametro as ParametroSchema, ParametroCreate, ParametroUpdate
from app.crud import parametro as crud_parametro

router = APIRouter()

@router.get("/parametros", response_model=List[ParametroSchema], tags=["Parametros"])
async def listar_parametros(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: AsyncSession = Depends(get_async_session)
):
    """Obtener lista de parámetros"""
    parametros = await crud_parametro.get_parametros(db, skip=skip, limit=limit)
    return parametros

@router.get("/parametros/{parametro_id}", response_model=ParametroSchema, tags=["Parametros"])
async def obtener_parametro(
    parametro_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Obtener un parámetro por ID"""
    parametro = await crud_parametro.get_parametro(db, parametro_id)
    if not parametro:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    return parametro

@router.get("/parametros/clave/{clave}", response_model=ParametroSchema, tags=["Parametros"])
async def obtener_parametro_por_clave(
    clave: str,
    db: AsyncSession = Depends(get_async_session)
):
    """Obtener un parámetro por clave"""
    parametro = await crud_parametro.get_parametro_by_clave(db, clave)
    if not parametro:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    return parametro

@router.post("/parametros", response_model=ParametroSchema, status_code=201, tags=["Parametros"])
async def crear_parametro(
    parametro: ParametroCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Crear un nuevo parámetro"""
    # Verificar que la clave no exista
    existente = await crud_parametro.get_parametro_by_clave(db, parametro.clave)
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un parámetro con esa clave")
    
    return await crud_parametro.create_parametro(db, parametro)

@router.put("/parametros/{parametro_id}", response_model=ParametroSchema, tags=["Parametros"])
async def actualizar_parametro(
    parametro_id: int,
    datos: ParametroUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Actualizar un parámetro existente"""
    # Si se está actualizando la clave, verificar que no exista otra con esa clave
    if datos.clave:
        existente = await crud_parametro.get_parametro_by_clave(db, datos.clave)
        if existente and existente.id != parametro_id:
            raise HTTPException(status_code=400, detail="Ya existe un parámetro con esa clave")
    
    actualizado = await crud_parametro.update_parametro(db, parametro_id, datos)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")
    return actualizado

@router.delete("/parametros/{parametro_id}", status_code=204, tags=["Parametros"])
async def eliminar_parametro(
    parametro_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Eliminar un parámetro"""
    eliminado = await crud_parametro.delete_parametro(db, parametro_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Parámetro no encontrado")