import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

class TestParametrosEndpoints:
    """Tests para las rutas de parámetros con mocks"""
    
    @pytest.fixture
    def mock_parametro(self):
        return {
            "id": 1,
            "clave": "TEST_PARAM",
            "valor": "valor_test",
            "descripcion": "Parámetro de prueba"
        }
    
    @patch("app.crud.parametro.create_parametro")
    @patch("app.crud.parametro.get_parametro_by_clave")
    def test_crear_parametro_exitoso(self, mock_get_by_clave, mock_crear_parametro, mock_parametro):
        """Test para crear un parámetro correctamente"""
        mock_get_by_clave.return_value = None  # No existe parámetro con esa clave
        mock_crear_parametro.return_value = mock_parametro
        
        payload = {
            "clave": "TEST_PARAM",
            "valor": "valor_test",
            "descripcion": "Parámetro de prueba"
        }
        
        response = client.post("/parametros", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["clave"] == "TEST_PARAM"
        assert data["valor"] == "valor_test"
        assert data["descripcion"] == "Parámetro de prueba"
    
    
    
    @patch("app.crud.parametro.get_parametros")
    def test_listar_parametros(self, mock_get_parametros, mock_parametro):
        """Test para listar parámetros"""
        mock_get_parametros.return_value = [mock_parametro]
        
        response = client.get("/parametros")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["clave"] == "TEST_PARAM"
  
    
    @patch("app.crud.parametro.get_parametro")
    def test_obtener_parametro_por_id_exitoso(self, mock_get_parametro, mock_parametro):
        """Test para obtener un parámetro por ID existente"""
        mock_get_parametro.return_value = mock_parametro
        
        response = client.get("/parametros/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["clave"] == "TEST_PARAM"
   
    
    @patch("app.crud.parametro.get_parametro_by_clave")
    def test_obtener_parametro_por_clave_exitoso(self, mock_get_by_clave, mock_parametro):
        """Test para obtener un parámetro por clave existente"""
        mock_get_by_clave.return_value = mock_parametro
        
        response = client.get("/parametros/clave/TEST_PARAM")
        assert response.status_code == 200
        data = response.json()
        assert data["clave"] == "TEST_PARAM"
        assert data["valor"] == "valor_test"
    
   
    
    @patch("app.crud.parametro.update_parametro")
    @patch("app.crud.parametro.get_parametro_by_clave")
    def test_actualizar_parametro_exitoso(self, mock_get_by_clave, mock_update_parametro, mock_parametro):
        """Test para actualizar un parámetro correctamente"""
        mock_get_by_clave.return_value = None  # No hay conflicto de clave
        
        # Crear mock object para el parámetro actualizado
        parametro_actualizado = MagicMock()
        parametro_actualizado.id = 1
        parametro_actualizado.clave = "TEST_PARAM"
        parametro_actualizado.valor = "nuevo_valor"
        parametro_actualizado.descripcion = "Descripción actualizada"
        
        mock_update_parametro.return_value = parametro_actualizado
        
        payload = {
            "valor": "nuevo_valor",
            "descripcion": "Descripción actualizada"
        }
        
        response = client.put("/parametros/1", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["valor"] == "nuevo_valor"
   
    
    
    @patch("app.crud.parametro.delete_parametro")
    def test_eliminar_parametro_exitoso(self, mock_delete_parametro):
        """Test para eliminar un parámetro existente"""
        mock_delete_parametro.return_value = True
        
        response = client.delete("/parametros/1")
        assert response.status_code == 204
   


if __name__ == "__main__":
    pytest.main([__file__, "-v"])