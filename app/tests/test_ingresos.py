import pytest
from fastapi.testclient import TestClient
from datetime import date
from unittest.mock import patch

from app.main import app

client = TestClient(app)


class TestIngresosEndpoints:
    """Tests para las rutas de ingresos con mocks"""

    @pytest.fixture
    def mock_ingreso(self):
        """Fixture con un ingreso de prueba"""
        return {
            "id": 6,
            "fecha": str(date.today()),
            "monto": 150.0,
            "descripcion": "Pago de habitación",
            "reserva_id": 2  # Este campo debe estar si tu schema IngresoRead lo requiere
        }

    @patch("app.crud.ingreso.crear_ingreso")
    def test_crear_ingreso_exitoso(self, mock_crear_ingreso, mock_ingreso):
        """Test para crear un ingreso correctamente"""
        mock_crear_ingreso.return_value = mock_ingreso

        payload = {
            "fecha": mock_ingreso["fecha"],
            "monto": mock_ingreso["monto"],
            "descripcion": mock_ingreso["descripcion"],
            "reserva_id": mock_ingreso["reserva_id"]  
        }

        response = client.post("/ingresos/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == mock_ingreso["id"]
        assert data["monto"] == mock_ingreso["monto"]
        assert data["descripcion"] == mock_ingreso["descripcion"]
        assert data["reserva_id"] == mock_ingreso["reserva_id"]


    @patch("app.crud.ingreso.obtener_ingresos")
    def test_listar_ingresos(self, mock_obtener_ingresos, mock_ingreso):
        """Test para listar ingresos"""
        mock_obtener_ingresos.return_value = [mock_ingreso]

        response = client.get("/ingresos/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == mock_ingreso["id"]
        assert data[0]["monto"] == mock_ingreso["monto"]
        assert data[0]["reserva_id"] == mock_ingreso["reserva_id"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
