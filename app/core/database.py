import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

connect_args = {}

# Evaluamos si estamos en SQLite o en PostgreSQL (Supabase) con asyncpg
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    # Configuración de SSL segura y compatible con asyncpg para Supabase
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Para asyncpg, pasamos el objeto SSLContext directamente en la llave "ssl"
    connect_args = {"ssl": ssl_context}

# Creamos el engine asíncrono
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=False,
    connect_args=connect_args
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session