import pytest
from fastapi.testclient import TestClient
from datetime import date, datetime, timedelta
from unittest.mock import AsyncMock, patch
import json

from main import app
from app.schemas.reportes import (
    LibroDiarioSchema,
    RegistroHuespedesSchema,
    RegistroOcupacionSchema,
    ResumenFinanciero,
    EstadisticasOcupacion
)

client = TestClient(app)



class TestReportesRoutes:
    """Tests para las rutas de reportes"""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock de la sesión de base de datos"""
        return AsyncMock()
    
    @pytest.fixture
    def libro_diario_mock_data(self):
        """Datos mock para libro diario"""
        return [
            {
                "fecha": "2024-01-15",
                "tipo": "Ingreso",
                "descripcion": "Pago reserva habitación 101",
                "monto": 150.00
            },
            {
                "fecha": "2024-01-15",
                "tipo": "Egreso", 
                "descripcion": "Compra suministros limpieza",
                "monto": 45.50
            }
        ]
    
    @pytest.fixture
    def registro_huespedes_mock_data(self):
        """Datos mock para registro de huéspedes"""
        return [
            {
                "cliente": "Juan Pérez",
                "documento_identidad": "1234567890",
                "correo": "juan@email.com",
                "telefono": "0999123456",
                "fecha_inicio": "2024-01-15",
                "fecha_fin": "2024-01-17",
                "habitacion": "101",
                "tipo_habitacion": "Simple",
                "estado_reserva": "Confirmada"
            }
        ]
    
    @pytest.fixture
    def registro_ocupacion_mock_data(self):
        """Datos mock para registro de ocupación"""
        return [
            {
                "habitacion": "101",
                "tipo": "Simple",
                "fecha_inicio": "2024-01-15",
                "fecha_fin": "2024-01-17",
                "estado_reserva": "Confirmada",
                "cliente": "Juan Pérez"
            }
        ]
    
    @pytest.fixture
    def resumen_financiero_mock_data(self):
        """Datos mock para resumen financiero"""
        return {
            "total_ingresos": 1500.00,
            "total_egresos": 450.00,
            "saldo": 1050.00,
            "periodo": "2024-01-01 - 2024-01-31"
        }
    
    @pytest.fixture
    def estadisticas_ocupacion_mock_data(self):
        """Datos mock para estadísticas de ocupación"""
        return {
            "total_reservas": 25,
            "habitaciones_ocupadas": 15,
            "habitaciones_disponibles": 5,
            "porcentaje_ocupacion": 75.0,
            "periodo": "2024-01-01 - 2024-01-31"
        }


class TestLibroDiarioEndpoint(TestReportesRoutes):
    """Tests para el endpoint de libro diario"""
    
    @patch('app.crud.reportes.obtener_libro_diario')
    def test_obtener_libro_diario_sin_filtros(self, mock_crud, libro_diario_mock_data):
        """Test para obtener libro diario sin filtros"""
        mock_crud.return_value = libro_diario_mock_data
        
        response = client.get("/reportes/libro-diario")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["tipo"] == "Ingreso"
        assert data[1]["tipo"] == "Egreso"
        mock_crud.assert_called_once()
    
    @patch('app.crud.reportes.obtener_libro_diario')
    def test_obtener_libro_diario_con_filtros_fecha(self, mock_crud, libro_diario_mock_data):
        """Test para obtener libro diario con filtros de fecha"""
        mock_crud.return_value = libro_diario_mock_data
        
        params = {
            "fecha_inicio": "2024-01-01",
            "fecha_fin": "2024-01-31"
        }
        response = client.get("/reportes/libro-diario", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        mock_crud.assert_called_once()
    
    @patch('app.crud.reportes.obtener_libro_diario')
    def test_obtener_libro_diario_filtro_tipo(self, mock_crud, libro_diario_mock_data):
        """Test para obtener libro diario filtrado por tipo"""
        mock_crud.return_value = [libro_diario_mock_data[0]]  # Solo ingresos
        
        params = {"tipo": "Ingreso"}
        response = client.get("/reportes/libro-diario", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["tipo"] == "Ingreso"


class TestRegistroHuespedesEndpoint(TestReportesRoutes):
    """Tests para el endpoint de registro de huéspedes"""
    
    @patch('app.crud.reportes.obtener_registro_huespedes')
    def test_obtener_registro_huespedes(self, mock_crud, registro_huespedes_mock_data):
        """Test para obtener registro de huéspedes"""
        mock_crud.return_value = registro_huespedes_mock_data
        
        response = client.get("/reportes/registro-huespedes")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["cliente"] == "Juan Pérez"
        assert data[0]["documento_identidad"] == "1234567890"
    
    @patch('app.crud.reportes.obtener_registro_huespedes')
    def test_obtener_registro_huespedes_filtro_documento(self, mock_crud, registro_huespedes_mock_data):
        """Test para obtener registro de huéspedes filtrado por documento"""
        mock_crud.return_value = registro_huespedes_mock_data
        
        params = {"documento_identidad": "1234567890"}
        response = client.get("/reportes/registro-huespedes", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["documento_identidad"] == "1234567890"
    
    @patch('app.crud.reportes.obtener_registro_huespedes')
    def test_obtener_registro_huespedes_filtro_nombre(self, mock_crud, registro_huespedes_mock_data):
        """Test para obtener registro de huéspedes filtrado por nombre"""
        mock_crud.return_value = registro_huespedes_mock_data
        
        params = {"nombre_cliente": "Juan"}
        response = client.get("/reportes/registro-huespedes", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Juan" in data[0]["cliente"]


class TestRegistroOcupacionEndpoint(TestReportesRoutes):
    """Tests para el endpoint de registro de ocupación"""
    
    @patch('app.crud.reportes.obtener_registro_ocupacion')
    def test_obtener_registro_ocupacion(self, mock_crud, registro_ocupacion_mock_data):
        """Test para obtener registro de ocupación"""
        mock_crud.return_value = registro_ocupacion_mock_data
        
        response = client.get("/reportes/registro-ocupacion")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["habitacion"] == "101"
        assert data[0]["estado_reserva"] == "Confirmada"
    
    @patch('app.crud.reportes.obtener_registro_ocupacion')
    def test_obtener_registro_ocupacion_filtro_habitacion(self, mock_crud, registro_ocupacion_mock_data):
        """Test para obtener registro de ocupación filtrado por habitación"""
        mock_crud.return_value = registro_ocupacion_mock_data
        
        params = {"numero_habitacion": "101"}
        response = client.get("/reportes/registro-ocupacion", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["habitacion"] == "101"
    
    @patch('app.crud.reportes.obtener_registro_ocupacion')
    def test_obtener_registro_ocupacion_filtro_tipo(self, mock_crud, registro_ocupacion_mock_data):
        """Test para obtener registro de ocupación filtrado por tipo"""
        mock_crud.return_value = registro_ocupacion_mock_data
        
        params = {"tipo_habitacion": "Simple"}
        response = client.get("/reportes/registro-ocupacion", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["tipo"] == "Simple"


class TestResumenFinancieroEndpoint(TestReportesRoutes):
    """Tests para el endpoint de resumen financiero"""
    
    @patch('app.crud.reportes.obtener_resumen_financiero')
    def test_obtener_resumen_financiero(self, mock_crud, resumen_financiero_mock_data):
        """Test para obtener resumen financiero"""
        mock_crud.return_value = resumen_financiero_mock_data
        
        response = client.get("/reportes/resumen-financiero")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_ingresos"] == 1500.00
        assert data["total_egresos"] == 450.00
        assert data["saldo"] == 1050.00
    
    @patch('app.crud.reportes.obtener_resumen_financiero')
    def test_obtener_resumen_financiero_con_fechas(self, mock_crud, resumen_financiero_mock_data):
        """Test para obtener resumen financiero con filtro de fechas"""
        mock_crud.return_value = resumen_financiero_mock_data
        
        params = {
            "fecha_inicio": "2024-01-01",
            "fecha_fin": "2024-01-31"
        }
        response = client.get("/reportes/resumen-financiero", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_ingresos" in data
        assert "total_egresos" in data
        assert "saldo" in data


class TestEstadisticasOcupacionEndpoint(TestReportesRoutes):
    """Tests para el endpoint de estadísticas de ocupación"""
    
    @patch('app.crud.reportes.obtener_estadisticas_ocupacion')
    def test_obtener_estadisticas_ocupacion(self, mock_crud, estadisticas_ocupacion_mock_data):
        """Test para obtener estadísticas de ocupación"""
        mock_crud.return_value = estadisticas_ocupacion_mock_data
        
        response = client.get("/reportes/estadisticas-ocupacion")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_reservas"] == 25
        assert data["habitaciones_ocupadas"] == 15
        assert data["porcentaje_ocupacion"] == 75.0
    
    @patch('app.crud.reportes.obtener_estadisticas_ocupacion')
    def test_obtener_estadisticas_ocupacion_con_fechas(self, mock_crud, estadisticas_ocupacion_mock_data):
        """Test para obtener estadísticas de ocupación con fechas"""
        mock_crud.return_value = estadisticas_ocupacion_mock_data
        
        params = {
            "fecha_inicio": "2024-01-01",
            "fecha_fin": "2024-01-31"
        }
        response = client.get("/reportes/estadisticas-ocupacion", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["porcentaje_ocupacion"] >= 0
        assert data["porcentaje_ocupacion"] <= 100


class TestExportacionEndpoint(TestReportesRoutes):
    """Tests para el endpoint de exportación"""
    
    @patch('app.crud.reportes.obtener_libro_diario')
    def test_exportar_libro_diario_json(self, mock_crud, libro_diario_mock_data):
        """Test para exportar libro diario en formato JSON"""
        mock_crud.return_value = libro_diario_mock_data
        
        params = {"formato": "json"}
        response = client.get("/reportes/libro-diario/exportar", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert data["formato"] == "json"
        assert data["total_registros"] == 2
        assert "datos" in data
        assert len(data["datos"]) == 2
    
    @patch('app.crud.reportes.obtener_libro_diario')
    def test_exportar_libro_diario_csv(self, mock_crud, libro_diario_mock_data):
        """Test para exportar libro diario en formato CSV (no implementado)"""
        mock_crud.return_value = libro_diario_mock_data
        
        params = {"formato": "csv"}
        response = client.get("/reportes/libro-diario/exportar", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert "CSV no implementada" in data["mensaje"]
        assert "datos" in data


class TestDashboardEndpoint(TestReportesRoutes):
    """Tests para el endpoint del dashboard"""
    
    @patch('app.crud.reportes.obtener_resumen_financiero')
    @patch('app.crud.reportes.obtener_estadisticas_ocupacion')
    @patch('app.crud.reportes.obtener_libro_diario')
    def test_obtener_dashboard(self, mock_libro, mock_estadisticas, mock_resumen,
                              resumen_financiero_mock_data, estadisticas_ocupacion_mock_data,
                              libro_diario_mock_data):
        """Test para obtener datos del dashboard"""
        mock_resumen.return_value = resumen_financiero_mock_data
        mock_estadisticas.return_value = estadisticas_ocupacion_mock_data
        mock_libro.return_value = libro_diario_mock_data
        
        response = client.get("/reportes/dashboard")
        
        assert response.status_code == 200
        data = response.json()
        assert "periodo" in data
        assert "resumen_financiero" in data
        assert "estadisticas_ocupacion" in data
        assert "ultimos_movimientos" in data
        assert "fecha_actualizacion" in data
        assert data["periodo"] == "Últimos 30 días"
    
    @patch('app.crud.reportes.obtener_resumen_financiero')
    @patch('app.crud.reportes.obtener_estadisticas_ocupacion')
    @patch('app.crud.reportes.obtener_libro_diario')
    def test_dashboard_ultimos_movimientos_limitados(self, mock_libro, mock_estadisticas, 
                                                   mock_resumen, libro_diario_mock_data):
        """Test para verificar que el dashboard limita los últimos movimientos a 10"""
        # Crear datos mock con más de 10 registros
        muchos_movimientos = libro_diario_mock_data * 6  # 12 registros
        mock_libro.return_value = muchos_movimientos
        mock_resumen.return_value = {}
        mock_estadisticas.return_value = {}
        
        response = client.get("/reportes/dashboard")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["ultimos_movimientos"]) == 10


class TestErrorHandling(TestReportesRoutes):
    """Tests para manejo de errores"""
    
    @patch('app.crud.reportes.obtener_libro_diario')
    def test_error_en_crud_libro_diario(self, mock_crud):
        """Test para manejar errores en CRUD de libro diario"""
        mock_crud.side_effect = Exception("Error de base de datos")
        
        response = client.get("/reportes/libro-diario")
        
        # El comportamiento exacto depende de cómo manejes los errores en tu app
        # Podrías esperar un 500 o un manejo específico de errores
        assert response.status_code in [500, 400, 422]
    
    def test_parametros_fecha_invalidos(self):
        """Test para parámetros de fecha inválidos"""
        params = {
            "fecha_inicio": "fecha-invalida",
            "fecha_fin": "2024-01-31"
        }
        response = client.get("/reportes/libro-diario", params=params)
        
        # FastAPI debería devolver 422 para parámetros inválidos
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])