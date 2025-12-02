from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.user import User, UserInDB
from ..core.config import settings
from ..database.connection import get_db
from ..database.models import User as DBUser

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_user(username: str, db: Optional[AsyncSession] = None) -> Optional[UserInDB]:
    """Get user from database."""
    if db is None:
        return None
    try:
        result = await db.execute(select(DBUser).where(DBUser.username == username))
        db_user = result.scalar_one_or_none()
        if db_user:
            return UserInDB(
                username=db_user.username,
                email=db_user.email,
                full_name=db_user.full_name,
                hashed_password=db_user.hashed_password,
                software_background=db_user.software_background,
                hardware_background=db_user.hardware_background,
                password=""  # Don't expose password
            )
    except Exception as e:
        print(f"Error getting user from DB: {e}")
        # Fallback to None if DB not available
    return None

async def authenticate_user(username: str, password: str, db: Optional[AsyncSession] = None):
    """Authenticate user with database."""
    if db is None:
        raise HTTPException(status_code=503, detail="Database not configured. Please set NEON_DB_URL.")
    user = await get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def create_user(user: User, db: Optional[AsyncSession] = None) -> UserInDB:
    """Create new user in database."""
    if db is None:
        raise HTTPException(status_code=503, detail="Database not configured. Please set NEON_DB_URL.")
    
    # Check if user exists
    existing = await get_user(user.username, db)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email exists (if provided)
    if user.email:
        result = await db.execute(select(DBUser).where(DBUser.email == user.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    
    # Create database user
    db_user = DBUser(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        software_background=user.software_background,
        hardware_background=user.hardware_background,
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return UserInDB(
        username=db_user.username,
        email=db_user.email,
        full_name=db_user.full_name,
        hashed_password=db_user.hashed_password,
        software_background=db_user.software_background,
        hardware_background=db_user.hardware_background,
        password=""
    )

async def get_user_by_id(user_id: str, db: Optional[AsyncSession] = None) -> Optional[UserInDB]:
    """Get user by username (used as user_id)."""
    return await get_user(user_id, db)

async def update_user_profile(
    username: str,
    software_background: Optional[str] = None,
    hardware_background: Optional[str] = None,
    db: Optional[AsyncSession] = None
) -> Optional[UserInDB]:
    """Update user profile in database."""
    if db is None:
        raise HTTPException(status_code=503, detail="Database not configured. Please set NEON_DB_URL.")
    
    result = await db.execute(select(DBUser).where(DBUser.username == username))
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        return None
    
    if software_background is not None:
        db_user.software_background = software_background
    if hardware_background is not None:
        db_user.hardware_background = hardware_background
    
    await db.commit()
    await db.refresh(db_user)
    
    return UserInDB(
        username=db_user.username,
        email=db_user.email,
        full_name=db_user.full_name,
        hashed_password=db_user.hashed_password,
        software_background=db_user.software_background,
        hardware_background=db_user.hardware_background,
        password=""
    )

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user(username, db)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    # In a real app, you'd check if the user is active
    return current_user
