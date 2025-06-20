import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def create_cliente():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/clientes/", json={
            "nombre": "Luis Rodríguez",
            "documento_identidad": "TEST001",
            "correo": "luis@test.com",
            "telefono": "0999999999"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Luis Rodríguez"
        assert data["documento_identidad"] == "TEST001"
        assert data["correo"] == "luis@test.com"
        assert data["telefono"] == "0999999999"

@pytest.mark.asyncio
async def get_cliente():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        crear = await client.post("/clientes/", json={
            "nombre": "Ana Vega",
            "documento_identidad": "TEST002",
            "correo": "ana@test.com",
            "telefono": "0888888888"
        })
        id_cliente = crear.json()["id"]

        response = await client.get(f"/clientes/{id_cliente}")
        assert response.status_code == 200
        assert response.json()["nombre"] == "Ana Vega"

@pytest.mark.asyncio
async def listar_clientes():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/clientes/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1