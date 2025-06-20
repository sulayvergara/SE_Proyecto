import pytest
from fastapi.testclient import TestClient
from datetime import date
from unittest.mock import patch
from app.main import app

client = TestClient(app)


class TestEgresosEndpoints:
    """Tests para las rutas de egresos con mocks"""

    @pytest.fixture
    def mock_egreso(self):
        return {
            "id": 10,
            "fecha": str(date.today()),
            "monto": 80.0,
            "descripcion": "Compra de insumos",
            "factura_id": 10  # este campo debe estar en tu schema si es requerido
        }

    @patch("app.crud.egreso.crear_egreso")
    def test_crear_egreso_exitoso(self, mock_crear_egreso, mock_egreso):
        """Test para crear un egreso correctamente"""
        mock_crear_egreso.return_value = mock_egreso

        payload = {
            "fecha": mock_egreso["fecha"],
            "monto": mock_egreso["monto"],
            "descripcion": mock_egreso["descripcion"],
            "factura_id": mock_egreso["factura_id"]
        }

        response = client.post("/egresos/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == mock_egreso["id"]
        assert data["monto"] == 80.0
        assert data["descripcion"] == "Compra de insumos"
        


    @patch("app.crud.egreso.obtener_egresos")
    def test_listar_egresos(self, mock_obtener_egresos, mock_egreso):
        """Test para listar egresos"""
        mock_obtener_egresos.return_value = [mock_egreso]

        response = client.get("/egresos/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["id"] == mock_egreso["id"]
        assert data[0]["monto"] == mock_egreso["monto"]
        assert data[0]["descripcion"] == mock_egreso["descripcion"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
