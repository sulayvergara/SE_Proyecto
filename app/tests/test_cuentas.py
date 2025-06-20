import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

class TestCuentasEndpoints:
    """Tests para las rutas de cuentas con mocks"""
    
    @pytest.fixture
    def mock_cuenta(self):
        return {
            "id": 1,
            "codigo": "1001",
            "nombre": "Caja General",
            "tipo": "activo",
            "nivel": 1
        }
    
    @pytest.fixture
    def mock_cuenta_lista(self, mock_cuenta):
        return [
            mock_cuenta,
            {
                "id": 2,
                "codigo": "1002",
                "nombre": "Bancos",
                "tipo": "activo",
                "nivel": 1
            }
        ]
    
    def create_mock_cuenta_object(self, **kwargs):
        """Helper method to create mock Cuenta objects with attributes"""
        mock_cuenta = MagicMock()
        default_values = {
            "id": 1,
            "codigo": "1001",
            "nombre": "Caja General",
            "tipo": "activo",
            "nivel": 1
        }
        default_values.update(kwargs)
        
        for key, value in default_values.items():
            setattr(mock_cuenta, key, value)
        
        return mock_cuenta
    
    @patch("app.crud.cuenta.crear_cuenta")
    @patch("app.crud.cuenta.obtener_cuenta_por_codigo")
    def test_crear_cuenta_exitoso(self, mock_obtener_por_codigo, mock_crear_cuenta, mock_cuenta):
        """Test para crear una cuenta correctamente"""
        mock_obtener_por_codigo.return_value = None  # No existe cuenta con ese código
        mock_crear_cuenta.return_value = mock_cuenta
        
        payload = {
            "codigo": "1001",
            "nombre": "Caja General",
            "tipo": "activo",
            "nivel": 1
        }
        
        response = client.post("/cuentas/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["codigo"] == "1001"
        assert data["nombre"] == "Caja General"
        assert data["tipo"] == "activo"
        assert data["nivel"] == 1
  
    
    @patch("app.crud.cuenta.obtener_cuenta")
    def test_obtener_cuenta_por_id_exitoso(self, mock_obtener_cuenta, mock_cuenta):
        """Test para obtener una cuenta por ID"""
        mock_obtener_cuenta.return_value = mock_cuenta
        
        response = client.get("/cuentas/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["codigo"] == "1001"
   
    
    @patch("app.crud.cuenta.obtener_cuenta_por_codigo")
    def test_obtener_cuenta_por_codigo_exitoso(self, mock_obtener_por_codigo, mock_cuenta):
        """Test para obtener una cuenta por código"""
        mock_obtener_por_codigo.return_value = mock_cuenta
        
        response = client.get("/cuentas/codigo/1001")
        assert response.status_code == 200
        data = response.json()
        assert data["codigo"] == "1001"
        assert data["nombre"] == "Caja General"
    
    
    @patch("app.crud.cuenta.listar_cuentas")
    def test_listar_cuentas(self, mock_listar_cuentas, mock_cuenta_lista):
        """Test para listar cuentas"""
        mock_listar_cuentas.return_value = mock_cuenta_lista
        
        response = client.get("/cuentas/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2
    
    
    @patch("app.crud.cuenta.buscar_cuentas")
    def test_buscar_cuentas(self, mock_buscar_cuentas, mock_cuenta):
        """Test para buscar cuentas"""
        mock_buscar_cuentas.return_value = [mock_cuenta]
        
        response = client.get("/cuentas/buscar/?q=caja")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["nombre"] == "Caja General"
   
    @patch("app.crud.cuenta.actualizar_cuenta")
    @patch("app.crud.cuenta.obtener_cuenta_por_codigo")
    def test_actualizar_cuenta_exitoso(self, mock_obtener_por_codigo, mock_actualizar_cuenta, mock_cuenta):
        """Test para actualizar una cuenta correctamente"""
        mock_obtener_por_codigo.return_value = None  # No existe otra cuenta con el nuevo código
        cuenta_actualizada = mock_cuenta.copy()
        cuenta_actualizada["nombre"] = "Caja General Actualizada"
        mock_actualizar_cuenta.return_value = cuenta_actualizada
        
        payload = {
            "nombre": "Caja General Actualizada"
        }
        
        response = client.put("/cuentas/1", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Caja General Actualizada"
   
    
    
    @patch("app.crud.cuenta.eliminar_cuenta")
    def test_eliminar_cuenta_exitoso(self, mock_eliminar_cuenta):
        """Test para eliminar una cuenta correctamente"""
        mock_eliminar_cuenta.return_value = True
        
        response = client.delete("/cuentas/1")
        assert response.status_code == 200
        data = response.json()
        assert data["mensaje"] == "Cuenta eliminada correctamente"
   
if __name__ == "__main__":
    pytest.main([__file__, "-v"])