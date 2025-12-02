# Neon DB Setup Guide

## ✅ Authentication is now connected to Neon DB!

All authentication and profile features now use Neon DB instead of in-memory storage.

## 🚀 Setup Steps

### 1. Set Neon DB URL in `.env`

Add your Neon DB connection string to `backend/.env`:

```env
NEON_DB_URL=postgresql://user:password@host/database
```

Or if Neon provides `postgres://`, that's fine - it will be automatically converted.

### 2. Initialize Database Tables

Run the initialization script to create the `users` table:

```bash
cd backend
python init_db.py
```

This will:
- Create the `users` table in your Neon DB
- Verify the table was created successfully

### 3. Start Backend

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 What's Changed

### ✅ Database Model
- **File**: `backend/src/database/models.py`
- SQLAlchemy `User` model with all fields

### ✅ Authentication Service
- **File**: `backend/src/services/auth_service.py`
- Now uses Neon DB instead of `fake_users_db`
- All functions are async and use database sessions
- Error handling for DB unavailability

### ✅ API Endpoints
- **Auth**: `backend/src/api/auth.py` - Sign in/Sign up now use DB
- **Profile**: `backend/src/api/profile.py` - New profile endpoints
  - `GET /api/v1/profile/{user_id}` - Get user profile
  - `PUT /api/v1/profile/{user_id}` - Update profile
- **Personalization**: `backend/src/api/personalization.py` - Now loads user from DB

### ✅ Frontend
- **Profile Component**: `my-ai-book/src/components/Profile.js`
- Now loads profile data from backend on mount
- Updates are saved to Neon DB

## 🎯 Features Now Using Neon DB

1. ✅ **User Registration** - Users saved to DB
2. ✅ **User Login** - Authentication from DB
3. ✅ **Profile Updates** - Saved to DB
4. ✅ **Personalization** - Loads user profile from DB
5. ✅ **User Persistence** - Data survives server restarts

## 🔍 Database Schema

```sql
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    full_name VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL,
    software_background TEXT,
    hardware_background TEXT
);
```

## ⚠️ Important Notes

1. **Database Required**: If `NEON_DB_URL` is not set, authentication endpoints will return 503 errors
2. **Migration**: Existing in-memory users need to be re-registered (they weren't persisted anyway)
3. **First Run**: Run `init_db.py` before starting the server for the first time

## 🧪 Testing

1. **Register a new user**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/users/ \
     -H "Content-Type: application/json" \
     -d '{"username": "test", "email": "test@example.com", "password": "test123", "software_background": "Python", "hardware_background": "Raspberry Pi"}'
   ```

2. **Login**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=test&password=test123"
   ```

3. **Get Profile**:
   ```bash
   curl http://localhost:8000/api/v1/profile/test
   ```

4. **Update Profile**:
   ```bash
   curl -X PUT http://localhost:8000/api/v1/profile/test \
     -H "Content-Type: application/json" \
     -d '{"software_background": "Python, JavaScript", "hardware_background": "Raspberry Pi, Arduino"}'
   ```

## ✅ All Done!

Your authentication system is now fully connected to Neon DB! 🎉

