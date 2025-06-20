import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta
from unittest.mock import patch

from app.main import app

client = TestClient(app)


class TestReservasEndpoints:
    """Tests para las rutas de reservas con mocks"""

    @pytest.fixture
    def mock_reserva(self):
        return {
            "id": 1,
            "cliente_id": 1,
            "habitacion_id": 1,
            "fecha_inicio": str(date.today()),
            "fecha_fin": str(date.today() + timedelta(days=2)),
            "estado": "reservada",
            "fecha_reserva": str(date.today())
        }

    @patch("app.crud.reserva.crear_reserva")
    def test_crear_reserva_exitoso(self, mock_crear_reserva, mock_reserva):
        """Test para crear una reserva correctamente"""
        mock_crear_reserva.return_value = mock_reserva
        payload = {
            "cliente_id": 1,
            "habitacion_id": 1,
            "fecha_inicio": mock_reserva["fecha_inicio"],
            "fecha_fin": mock_reserva["fecha_fin"]
        }
        response = client.post("/reservas/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["cliente_id"] == 1
        assert data["habitacion_id"] == 1
        assert data["estado"] == "reservada"

    @patch("app.crud.reserva.obtener_reservas")
    def test_listar_reservas(self, mock_obtener_reservas, mock_reserva):
        """Test para listar reservas"""
        mock_obtener_reservas.return_value = [mock_reserva]
        response = client.get("/reservas/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["id"] == 1

    @patch("app.crud.reserva.cancelar_reserva")
    def test_cancelar_reserva_valida(self, mock_cancelar_reserva, mock_reserva):
        """Test para cancelar una reserva existente"""
        mock_reserva["estado"] = "cancelada"
        mock_cancelar_reserva.return_value = mock_reserva
        response = client.put("/reservas/1/cancelar")
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "cancelada"

    @patch("app.crud.reserva.cancelar_reserva")
    def test_cancelar_reserva_inexistente(self, mock_cancelar_reserva):
        """Test para cancelar una reserva inexistente"""
        mock_cancelar_reserva.return_value = None
        response = client.put("/reservas/999/cancelar")
        assert response.status_code == 404
        assert response.json()["detail"] == "Reserva no encontrada"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])