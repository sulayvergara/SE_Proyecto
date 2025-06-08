from fastapi import FastAPI
from app.database import engine, Base
from app.routers import habitacion
from app.routers import cliente

app = FastAPI(title="Sistema de Reservas de Hoteles")

# (Opcional) Evento startup para crear tablas automáticamente
@app.on_event("startup")
async def on_startup():
    # Crea las tablas que declares en tus modelos (si no existen)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/",tags=["Bienvenida"])
async def root():
    return {"mensaje": "¡Bienvenido al Sistema de Reservas!"}

app.include_router(habitacion.router)
#app.include_router(cliente.router)