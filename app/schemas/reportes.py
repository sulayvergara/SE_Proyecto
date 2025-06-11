from pydantic import BaseModel
from datetime import date
from typing import Optional
from decimal import Decimal

class LibroDiarioSchema(BaseModel):
    fecha: date
    tipo: str
    descripcion: Optional[str] = None
    monto: Decimal

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: float
        }


class RegistroHuespedesSchema(BaseModel):
    cliente: str
    documento_identidad: str
    correo: Optional[str] = None
    telefono: Optional[str] = None
    fecha_inicio: date
    fecha_fin: date
    habitacion: str
    tipo_habitacion: str
    estado_reserva: str

    class Config:
        from_attributes = True


class RegistroOcupacionSchema(BaseModel):
    habitacion: str
    tipo: str
    fecha_inicio: date
    fecha_fin: date
    estado_reserva: str
    cliente: str

    class Config:
        from_attributes = True


# Esquemas para filtros de reportes
class FiltroFechas(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class FiltroHuesped(BaseModel):
    documento_identidad: Optional[str] = None
    nombre_cliente: Optional[str] = None


class FiltroHabitacion(BaseModel):
    numero_habitacion: Optional[str] = None
    tipo_habitacion: Optional[str] = None


# Esquemas de respuesta para reportes con totales
class ResumenFinanciero(BaseModel):
    total_ingresos: Decimal
    total_egresos: Decimal
    saldo: Decimal
    periodo: str

    class Config:
        json_encoders = {
            Decimal: float
        }


class EstadisticasOcupacion(BaseModel):
    total_reservas: int
    habitaciones_ocupadas: int
    habitaciones_disponibles: int
    porcentaje_ocupacion: float
    periodo: str