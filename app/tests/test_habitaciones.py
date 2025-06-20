import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_crear_habitacion():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/habitaciones/", json={
            "numero": "401",
            "tipo": "doble",
            "precio_noche": 80.0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["numero"] == "401"
        assert data["tipo"] == "doble"
        assert float(data["precio_noche"]) == 80.0
        assert data["estado"] == "disponible"

@pytest.mark.asyncio
async def test_obtener_habitacion_por_id():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Crear primero
        crear = await client.post("/habitaciones/", json={
            "numero": "402",
            "tipo": "suite",
            "precio_noche": 150.0
        })
        id_hab = crear.json()["id"]

        # Obtener por ID
        response = await client.get(f"/habitaciones/{id_hab}")
        assert response.status_code == 200
        assert response.json()["numero"] == "402"

@pytest.mark.asyncio
async def test_actualizar_estado_habitacion():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Crear
        crear = await client.post("/habitaciones/", json={
            "numero": "403",
            "tipo": "simple",
            "precio_noche": 60.0
        })
        id_hab = crear.json()["id"]

        # Cambiar estado
        response = await client.put(f"/habitaciones/{id_hab}/estado?nuevo_estado=ocupada")
        assert response.status_code == 200
        assert response.json()["estado"] == "ocupada"

@pytest.mark.asyncio
async def test_listar_habitaciones():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/habitaciones/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # ya hay habitaciones creadas
