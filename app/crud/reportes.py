from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, func, text
from app.models.reportes import VistaLibroDiario, VistaRegistroHuespedes, VistaRegistroOcupacion
from app.models.habitacion import Habitacion
from app.schemas.reportes import (
    LibroDiarioSchema, 
    RegistroHuespedesSchema, 
    RegistroOcupacionSchema,
    ResumenFinanciero,
    EstadisticasOcupacion
)
from typing import List, Optional
from datetime import date
from decimal import Decimal


async def obtener_libro_diario(
    db: AsyncSession, 
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    tipo: Optional[str] = None
) -> List[VistaLibroDiario]:
    """Obtener registros del libro diario con filtros opcionales"""
    query = select(VistaLibroDiario)
    
    conditions = []
    if fecha_inicio:
        conditions.append(VistaLibroDiario.fecha >= fecha_inicio)
    if fecha_fin:
        conditions.append(VistaLibroDiario.fecha <= fecha_fin)
    if tipo:
        conditions.append(VistaLibroDiario.tipo == tipo)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.order_by(VistaLibroDiario.fecha.desc())
    
    result = await db.execute(query)
    return result.scalars().all()


async def obtener_registro_huespedes(
    db: AsyncSession,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    documento_identidad: Optional[str] = None,
    nombre_cliente: Optional[str] = None
) -> List[VistaRegistroHuespedes]:
    """Obtener registro de huéspedes con filtros opcionales"""
    query = select(VistaRegistroHuespedes)
    
    conditions = []
    if fecha_inicio:
        conditions.append(VistaRegistroHuespedes.fecha_inicio >= fecha_inicio)
    if fecha_fin:
        conditions.append(VistaRegistroHuespedes.fecha_fin <= fecha_fin)
    if documento_identidad:
        conditions.append(VistaRegistroHuespedes.documento_identidad == documento_identidad)
    if nombre_cliente:
        conditions.append(VistaRegistroHuespedes.cliente.ilike(f"%{nombre_cliente}%"))
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.order_by(VistaRegistroHuespedes.fecha_inicio.desc())
    
    result = await db.execute(query)
    return result.scalars().all()


async def obtener_registro_ocupacion(
    db: AsyncSession,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    numero_habitacion: Optional[str] = None,
    tipo_habitacion: Optional[str] = None
) -> List[VistaRegistroOcupacion]:
    """Obtener registro de ocupación con filtros opcionales"""
    query = select(VistaRegistroOcupacion)
    
    conditions = []
    if fecha_inicio:
        conditions.append(VistaRegistroOcupacion.fecha_inicio >= fecha_inicio)
    if fecha_fin:
        conditions.append(VistaRegistroOcupacion.fecha_fin <= fecha_fin)
    if numero_habitacion:
        conditions.append(VistaRegistroOcupacion.habitacion == numero_habitacion)
    if tipo_habitacion:
        conditions.append(VistaRegistroOcupacion.tipo.ilike(f"%{tipo_habitacion}%"))
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.order_by(VistaRegistroOcupacion.habitacion, VistaRegistroOcupacion.fecha_inicio.desc())
    
    result = await db.execute(query)
    return result.scalars().all()


async def obtener_resumen_financiero(
    db: AsyncSession,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None
) -> ResumenFinanciero:
    """Obtener resumen financiero con totales de ingresos y egresos"""
    
    # Query para obtener totales usando SQL directo para mayor flexibilidad
    query_ingresos = text("""
        SELECT COALESCE(SUM(monto), 0) as total_ingresos
        FROM ingresos
        WHERE (:fecha_inicio IS NULL OR fecha >= :fecha_inicio)
        AND (:fecha_fin IS NULL OR fecha <= :fecha_fin)
    """)
    
    query_egresos = text("""
        SELECT COALESCE(SUM(monto), 0) as total_egresos
        FROM egresos
        WHERE (:fecha_inicio IS NULL OR fecha >= :fecha_inicio)
        AND (:fecha_fin IS NULL OR fecha <= :fecha_fin)
    """)
    
    # Ejecutar queries
    result_ingresos = await db.execute(
        query_ingresos, 
        {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin}
    )
    result_egresos = await db.execute(
        query_egresos, 
        {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin}
    )
    
    total_ingresos = result_ingresos.scalar() or Decimal('0')
    total_egresos = result_egresos.scalar() or Decimal('0')
    saldo = total_ingresos - total_egresos
    
    # Determinar el periodo
    if fecha_inicio and fecha_fin:
        periodo = f"{fecha_inicio} - {fecha_fin}"
    elif fecha_inicio:
        periodo = f"Desde {fecha_inicio}"
    elif fecha_fin:
        periodo = f"Hasta {fecha_fin}"
    else:
        periodo = "Todo el tiempo"
    
    return ResumenFinanciero(
        total_ingresos=total_ingresos,
        total_egresos=total_egresos,
        saldo=saldo,
        periodo=periodo
    )


async def obtener_estadisticas_ocupacion(
    db: AsyncSession,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None
) -> EstadisticasOcupacion:
    """Obtener estadísticas de ocupación de habitaciones"""
    
    # Total de habitaciones
    query_total_habitaciones = select(func.count(Habitacion.id))
    result_total = await db.execute(query_total_habitaciones)
    total_habitaciones = result_total.scalar()
    
    # Query para reservas en el período
    query_reservas = text("""
        SELECT COUNT(*) as total_reservas,
               COUNT(DISTINCT habitacion_id) as habitaciones_ocupadas
        FROM reservas
        WHERE estado IN ('reservada', 'completada')
        AND (:fecha_inicio IS NULL OR fecha_inicio >= :fecha_inicio)
        AND (:fecha_fin IS NULL OR fecha_fin <= :fecha_fin)
    """)
    
    result_reservas = await db.execute(
        query_reservas,
        {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin}
    )
    
    row = result_reservas.fetchone()
    total_reservas = row[0] if row else 0
    habitaciones_ocupadas = row[1] if row else 0
    
    habitaciones_disponibles = total_habitaciones - habitaciones_ocupadas
    porcentaje_ocupacion = (habitaciones_ocupadas / total_habitaciones * 100) if total_habitaciones > 0 else 0
    
    # Determinar el periodo
    if fecha_inicio and fecha_fin:
        periodo = f"{fecha_inicio} - {fecha_fin}"
    elif fecha_inicio:
        periodo = f"Desde {fecha_inicio}"
    elif fecha_fin:
        periodo = f"Hasta {fecha_fin}"
    else:
        periodo = "Todo el tiempo"
    
    return EstadisticasOcupacion(
        total_reservas=total_reservas,
        habitaciones_ocupadas=habitaciones_ocupadas,
        habitaciones_disponibles=habitaciones_disponibles,
        porcentaje_ocupacion=round(porcentaje_ocupacion, 2),
        periodo=periodo
    )