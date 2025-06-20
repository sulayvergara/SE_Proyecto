import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import sys
import os

# Agregar el directorio raíz al path si es necesario
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.main import app
except ImportError:
    # Fallback si hay problemas con el import
    from fastapi import FastAPI
    app = FastAPI()

client = TestClient(app)

class TestUsuariosEndpoints:
    """Tests para las rutas de usuarios con mocks"""
    
    @pytest.fixture
    def mock_usuario(self):
        return {
            "id": 1,
            "nombre": "Juan Pérez",
            "correo": "juan.perez@email.com",
            "rol_id": 1
        }
    
    @pytest.fixture
    def mock_usuario_create(self):
        return {
            "nombre": "Juan Pérez",
            "correo": "juan.perez@email.com",
            "contraseña": "password123",
            "rol_id": 1
        }
    
    def test_crear_usuario_exitoso(self, mock_usuario, mock_usuario_create):
        """Test para crear un usuario correctamente"""
        with patch("app.crud.usuario.obtener_usuario_correo", new_callable=AsyncMock) as mock_obtener_usuario_correo, \
             patch("app.crud.usuario.crear_usuario", new_callable=AsyncMock) as mock_crear_usuario:
            
            mock_obtener_usuario_correo.return_value = None  # Usuario no existe
            mock_crear_usuario.return_value = mock_usuario
            
            response = client.post("/usuarios/", json=mock_usuario_create)
            
            assert response.status_code == 200
            data = response.json()
            assert data["nombre"] == "Juan Pérez"
            assert data["correo"] == "juan.perez@email.com"
            assert data["rol_id"] == 1
            assert data["id"] == 1
    
    
    def test_listar_usuarios(self, mock_usuario):
        """Test para listar usuarios"""
        with patch("app.crud.usuario.listar_usuarios", new_callable=AsyncMock) as mock_listar_usuarios:
            mock_listar_usuarios.return_value = [mock_usuario]
            
            response = client.get("/usuarios/")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]["id"] == 1
            assert data[0]["nombre"] == "Juan Pérez"
    
    def test_obtener_usuario_existente(self, mock_usuario):
        """Test para obtener un usuario existente"""
        with patch("app.crud.usuario.obtener_usuario", new_callable=AsyncMock) as mock_obtener_usuario:
            mock_obtener_usuario.return_value = mock_usuario
            
            response = client.get("/usuarios/1")
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["nombre"] == "Juan Pérez"
            assert data["correo"] == "juan.perez@email.com"
    

    
    def test_obtener_usuario_por_correo_existente(self, mock_usuario):
        """Test para obtener un usuario por correo existente"""
        with patch("app.crud.usuario.obtener_usuario_correo", new_callable=AsyncMock) as mock_obtener_usuario_correo:
            mock_obtener_usuario_correo.return_value = mock_usuario
            
            response = client.get("/usuarios/por-correo/?correo=juan.perez@email.com")
            
            assert response.status_code == 200
            data = response.json()
            assert data["correo"] == "juan.perez@email.com"
            assert data["nombre"] == "Juan Pérez"
    

    def test_actualizar_usuario_exitoso(self, mock_usuario, mock_usuario_create):
        """Test para actualizar un usuario existente"""
        with patch("app.crud.usuario.actualizar_usuario", new_callable=AsyncMock) as mock_actualizar_usuario:
            usuario_actualizado = mock_usuario.copy()
            usuario_actualizado["nombre"] = "Juan Carlos Pérez"
            mock_actualizar_usuario.return_value = usuario_actualizado
            
            datos_actualizacion = mock_usuario_create.copy()
            datos_actualizacion["nombre"] = "Juan Carlos Pérez"
            
            response = client.put("/usuarios/1", json=datos_actualizacion)
            
            assert response.status_code == 200
            data = response.json()
            assert data["nombre"] == "Juan Carlos Pérez"
            assert data["id"] == 1
    
    def test_eliminar_usuario_existente(self):
        """Test para eliminar un usuario existente"""
        with patch("app.crud.usuario.eliminar_usuario", new_callable=AsyncMock) as mock_eliminar_usuario:
            mock_eliminar_usuario.return_value = True
            
            response = client.delete("/usuarios/1")
            
            assert response.status_code == 200
            data = response.json()
            assert data["mensaje"] == "Usuario eliminado"
    
    


if __name__ == "__main__":
    pytest.main([__file__, "-v"])