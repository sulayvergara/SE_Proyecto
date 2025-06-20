import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


class TestHabitacionesEndpoints:
    """Tests para las rutas de habitaciones con mocks"""

    @pytest.fixture
    def mock_habitacion(self):
        return {
            "id": 1,
            "numero": "101",
            "tipo": "simple",
            "precio_noche": 50.0,
            "estado": "disponible"
        }

    @patch("app.crud.habitacion.crear_habitacion")
    def test_crear_habitacion_exitoso(self, mock_crear_habitacion, mock_habitacion):
        """Test para crear una habitación correctamente"""
        mock_crear_habitacion.return_value = mock_habitacion
        payload = {
            "numero": "101",
            "tipo": "simple",
            "precio_noche": 50.0
        }
        response = client.post("/habitaciones/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["numero"] == "101"
        assert data["tipo"] == "simple"
        assert data["precio_noche"] == 50.0

    @patch("app.crud.habitacion.obtener_habitaciones")
    def test_listar_habitaciones(self, mock_obtener_habitaciones, mock_habitacion):
        """Test para listar habitaciones"""
        mock_obtener_habitaciones.return_value = [mock_habitacion]
        response = client.get("/habitaciones/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["id"] == 1

    @patch("app.crud.habitacion.obtener_habitacion_por_id")
    def test_obtener_habitacion_por_id(self, mock_obtener_por_id, mock_habitacion):
        """Test para obtener habitación por ID"""
        mock_obtener_por_id.return_value = mock_habitacion
        response = client.get("/habitaciones/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["numero"] == "101"

    @patch("app.crud.habitacion.obtener_habitacion_por_id")
    def test_obtener_habitacion_inexistente(self, mock_obtener_por_id):
        """Test para obtener habitación no existente"""
        mock_obtener_por_id.return_value = None
        response = client.get("/habitaciones/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Habitación no encontrada"

    @patch("app.crud.habitacion.actualizar_estado_habitacion")
    def test_actualizar_estado_habitacion(self, mock_actualizar_estado, mock_habitacion):
        """Test para actualizar el estado de una habitación"""
        mock_habitacion["estado"] = "ocupada"
        mock_actualizar_estado.return_value = mock_habitacion
        response = client.put("/habitaciones/1/estado?nuevo_estado=ocupada")
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "ocupada"

    @patch("app.crud.habitacion.actualizar_estado_habitacion")
    def test_actualizar_estado_habitacion_inexistente(self, mock_actualizar_estado):
        """Test para actualizar estado de habitación inexistente"""
        mock_actualizar_estado.return_value = None
        response = client.put("/habitaciones/999/estado?nuevo_estado=ocupada")
        assert response.status_code == 404
        assert response.json()["detail"] == "Habitación no encontrada"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
