from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.usuario import UsuarioCreate, Usuario, UsuarioCorreo
from app.crud import usuario as crud_usuario
from app.database import get_async_session
from typing import List
from pydantic import EmailStr

router = APIRouter(tags=["Usuarios"])

@router.post("/usuarios/", response_model=Usuario, tags=["Usuarios"])
async def crear_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_async_session)):
    existente = await crud_usuario.obtener_usuario_correo(db, usuario.correo)
    if existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return await crud_usuario.crear_usuario(db, usuario)

@router.get("/usuarios/", response_model=List[Usuario], tags=["Usuarios"])
async def listar_usuarios(db: AsyncSession = Depends(get_async_session)):
    return await crud_usuario.listar_usuarios(db)

@router.get("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(get_async_session)):
    usuario = await crud_usuario.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Corregido: cambiada la ruta para evitar conflicto con el endpoint anterior
@router.get("/usuarios/por-correo/", response_model=Usuario, tags=["Usuarios"])
async def obtener_usuario_correo(correo: EmailStr = Query(...), db: AsyncSession = Depends(get_async_session)):
    usuario = await crud_usuario.obtener_usuario_correo(db, correo)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
async def actualizar_usuario(usuario_id: int, datos: UsuarioCreate, db: AsyncSession = Depends(get_async_session)):
    actualizado = await crud_usuario.actualizar_usuario(db, usuario_id, datos)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return actualizado

@router.delete("/usuarios/{usuario_id}", tags=["Usuarios"])
async def eliminar_usuario(usuario_id: int, db: AsyncSession = Depends(get_async_session)):
    eliminado = await crud_usuario.eliminar_usuario(db, usuario_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}