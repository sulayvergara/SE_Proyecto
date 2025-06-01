from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno del .env

DATABASE_URL = os.getenv("DATABASE_URL")

# Creamos un motor asíncrono para PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True)

# sessionmaker configurado para usar AsyncSession
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()

# Dependencia de FastAPI para obtener la sesión de DB en cada request
async def get_db():
    async with SessionLocal() as session:
        yield session
