from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.schemas.reportes import (
    LibroDiarioSchema,
    RegistroHuespedesSchema,
    RegistroOcupacionSchema,
    ResumenFinanciero,
    EstadisticasOcupacion
)
from app.crud import reportes as crud_reportes
from typing import List, Optional
from datetime import date

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/libro-diario", response_model=List[LibroDiarioSchema])
async def obtener_libro_diario(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio del período"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin del período"),
    tipo: Optional[str] = Query(None, description="Tipo de movimiento: 'Ingreso' o 'Egreso'"),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Obtener el libro diario con todos los movimientos de ingresos y egresos.
    Permite filtrar por fechas y tipo de movimiento.
    """
    return await crud_reportes.obtener_libro_diario(
        db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, tipo=tipo
    )


@router.get("/registro-huespedes", response_model=List[RegistroHuespedesSchema])
async def obtener_registro_huespedes(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio de la reserva"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin de la reserva"),
    documento_identidad: Optional[str] = Query(None, description="Documento de identidad del huésped"),
    nombre_cliente: Optional[str] = Query(None, description="Nombre del cliente (búsqueda parcial)"),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Obtener el registro completo de huéspedes con sus reservas.
    Permite filtrar por fechas, documento de identidad o nombre del cliente.
    """
    return await crud_reportes.obtener_registro_huespedes(
        db, 
        fecha_inicio=fecha_inicio, 
        fecha_fin=fecha_fin,
        documento_identidad=documento_identidad,
        nombre_cliente=nombre_cliente
    )


@router.get("/registro-ocupacion", response_model=List[RegistroOcupacionSchema])
async def obtener_registro_ocupacion(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio del período"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin del período"),
    numero_habitacion: Optional[str] = Query(None, description="Número de habitación específica"),
    tipo_habitacion: Optional[str] = Query(None, description="Tipo de habitación"),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Obtener el registro de ocupación de habitaciones.
    Muestra qué habitaciones han estado ocupadas y por quién.
    """
    return await crud_reportes.obtener_registro_ocupacion(
        db,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        numero_habitacion=numero_habitacion,
        tipo_habitacion=tipo_habitacion
    )


@router.get("/resumen-financiero", response_model=ResumenFinanciero)
async def obtener_resumen_financiero(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio del período"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin del período"),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Obtener un resumen financiero con totales de ingresos, egresos y saldo.
    Útil para tener una vista general de la situación financiera del hotel.
    """
    return await crud_reportes.obtener_resumen_financiero(
        db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
    )


@router.get("/estadisticas-ocupacion", response_model=EstadisticasOcupacion)
async def obtener_estadisticas_ocupacion(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio del período"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin del período"),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Obtener estadísticas de ocupación de habitaciones.
    Incluye total de reservas, habitaciones ocupadas, disponibles y porcentaje de ocupación.
    """
    return await crud_reportes.obtener_estadisticas_ocupacion(
        db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
    )


# Endpoints adicionales para exportación de reportes
@router.get("/libro-diario/exportar")
async def exportar_libro_diario(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    tipo: Optional[str] = Query(None),
    formato: str = Query("json", description="Formato de exportación: json, csv"),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Exportar el libro diario en diferentes formatos.
    Por ahora solo soporta JSON, pero se puede extender para CSV o Excel.
    """
    datos = await crud_reportes.obtener_libro_diario(
        db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, tipo=tipo
    )
    
    if formato.lower() == "csv":
        # Aquí se podría implementar la conversión a CSV
        # Por ahora retornamos un mensaje indicativo
        return {"mensaje": "Exportación a CSV no implementada aún", "datos": datos}
    
    return {
        "formato": formato,
        "total_registros": len(datos),
        "periodo": f"{fecha_inicio or 'inicio'} - {fecha_fin or 'fin'}",
        "datos": datos
    }


@router.get("/dashboard")
async def obtener_dashboard(
    db: AsyncSession = Depends(get_async_session)
):
    """
    Endpoint para obtener datos del dashboard principal.
    Combina varios reportes en una sola respuesta para mostrar métricas clave.
    """
    # Obtener datos de los últimos 30 días
    from datetime import datetime, timedelta
    fecha_fin = date.today()
    fecha_inicio = fecha_fin - timedelta(days=30)
    
    resumen_financiero = await crud_reportes.obtener_resumen_financiero(
        db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
    )
    
    estadisticas_ocupacion = await crud_reportes.obtener_estadisticas_ocupacion(
        db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
    )
    
    # Obtener últimos movimientos (últimos 10)
    ultimos_movimientos = await crud_reportes.obtener_libro_diario(db)
    ultimos_movimientos = ultimos_movimientos[:10]  # Solo los últimos 10
    
    return {
        "periodo": "Últimos 30 días",
        "resumen_financiero": resumen_financiero,
        "estadisticas_ocupacion": estadisticas_ocupacion,
        "ultimos_movimientos": ultimos_movimientos,
        "fecha_actualizacion": datetime.now()
    }