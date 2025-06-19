from fastapi.testclient import TestClient
from app.main import app

def test_crear_habitacion():
    client = TestClient(app)
    response = client.post("/habitaciones/", json={
        "numero": "302",
        "tipo": "simple",
        "precio_noche": 55.00
    })
    assert response.status_code == 200
    assert response.json()["numero"] == "302"
