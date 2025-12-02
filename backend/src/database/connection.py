from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

# Lazy initialization - don't create engine at import time to prevent hanging
engine = None
AsyncSessionLocal = None


def _make_async_url(url: str) -> str:
    """
    Ensure the database URL uses an async driver.

    Neon typically provides URLs like:
      postgres://user:pass@host/db
    or:
      postgresql://user:pass@host/db

    For SQLAlchemy asyncio with asyncpg, we need:
      postgresql+asyncpg://user:pass@host/db
    """
    if not url:
        return ""

    if "+asyncpg" in url:
        return url

    if url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + url[len("postgresql://") :]

    if url.startswith("postgres://"):
        # Alias often used by Neon; normalize to postgresql+asyncpg
        return "postgresql+asyncpg://" + url[len("postgres://") :]

    # Fallback: return as-is (for non-Postgres drivers)
    return url


def _init_db_if_needed():
    """Initialize database connection only when needed, not at import time."""
    global engine, AsyncSessionLocal
    
    if engine is not None:
        return  # Already initialized
    
    async_db_url = _make_async_url(settings.NEON_DB_URL)
    
    if not async_db_url:
        # No database URL configured - database features disabled
        return
    
    try:
        # Create engine with settings to prevent hanging
        engine = create_async_engine(
            async_db_url,
            echo=False,  # Disable echo to reduce startup noise
            pool_pre_ping=True,  # Verify connections before using
        )

        # Create a sessionmaker bound to the engine for async sessions
        AsyncSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    except Exception as e:
        # If engine creation fails, log but don't crash
        print(f"Warning: Could not initialize database connection: {e}")
        print("Database features will be disabled. Set NEON_DB_URL to enable.")


async def get_db():
    """Get database session, initializing connection if needed."""
    _init_db_if_needed()
    
    if AsyncSessionLocal is None:
        raise RuntimeError(
            "Async database session is not configured. "
            "Please set a valid NEON_DB_URL (e.g. postgresql://... from Neon) in your .env file."
        )

    async with AsyncSessionLocal() as session:
        yield session
