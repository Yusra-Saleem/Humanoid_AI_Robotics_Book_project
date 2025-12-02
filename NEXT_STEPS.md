# 🚀 Next Steps - Complete Setup Guide

## ✅ What's Done

1. ✅ **Authentication** - Connected to Neon DB
2. ✅ **Database Models** - User table ready
3. ✅ **Profile API** - Save/load from DB
4. ✅ **Personalization** - Loads user from DB
5. ✅ **Translation** - Urdu translation working
6. ✅ **Text Selection** - Ask questions about selected text
7. ✅ **Markdown Ingestion** - Script ready

## 📋 Step-by-Step Setup

### Step 1: Environment Variables Setup

Create/update `backend/.env` file:

```env
# OpenAI API Key (Required for chatbot, translation, personalization)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Neon DB (Required for authentication and profiles)
NEON_DB_URL=postgresql://user:password@host/database

# Qdrant (Required for RAG chatbot)
# Option 1: Qdrant Cloud
QDRANT_URL=https://your-cluster-id.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key

# Option 2: Local Qdrant (if running locally)
# QDRANT_HOST=localhost
# QDRANT_PORT=6333

# Qdrant Collection Name (optional, defaults to "textbook_chunks")
QDRANT_COLLECTION_NAME=textbook_chunks

# JWT Secret (for authentication tokens)
SECRET_KEY=your-secret-key-here-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS (for frontend)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Initialize Database

```bash
cd backend
python init_db.py
```

**Expected Output:**
```
Initializing database...
✅ Database tables created successfully!
✅ Users table verified!
```

### Step 4: Ingest Markdown Files into Qdrant

```bash
cd backend
python ingest_docs.py
```

**Expected Output:**
```
Loading FastEmbed model...
✓ FastEmbed model loaded
Connecting to Qdrant Cloud: https://...
✓ Qdrant client initialized
✓ Collection 'textbook_chunks' already exists
Processing: 01-Week-3-Nodes-Topics.md
  → Generated 15 chunks
  ✓ Ingested 15 chunks into Qdrant
...
✅ Ingestion complete! Total files processed: X
Chatbot will retrieve relevant context from Qdrant based on your queries.
```

### Step 5: Start Backend Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Check if everything is working:**
```bash
curl http://localhost:8000/api/v1/config/check
```

**Expected Response:**
```json
{
  "openai_configured": true,
  "key_preview": "sk-xxxx...xxxx",
  "key_valid": true,
  "key_error": null,
  "qdrant_configured": true,
  "neon_db_configured": true
}
```

### Step 6: Start Frontend

```bash
cd my-ai-book
npm install  # If not already done
npm start
```

Frontend will open at `http://localhost:3000`

## 🧪 Testing Checklist

### ✅ Authentication
- [ ] Sign Up - Create new user account
- [ ] Sign In - Login with credentials
- [ ] Check localStorage - `user_id` and `token` should be saved
- [ ] Profile - View and update profile

### ✅ Chatbot
- [ ] Open chatbot on docs page
- [ ] Ask a question about textbook content
- [ ] Check if answer includes sources/references
- [ ] Test text selection - Select text and click "Ask"
- [ ] Verify selected text is explained with references

### ✅ Personalization
- [ ] Update profile (hardware/software background)
- [ ] Use personalization feature
- [ ] Verify content is adapted based on profile

### ✅ Translation
- [ ] Go to `/translate` page
- [ ] Enter English text
- [ ] Click "Translate to Urdu"
- [ ] Verify Urdu translation appears

### ✅ Database Persistence
- [ ] Create user account
- [ ] Restart backend server
- [ ] Login again - Should work (data persisted in DB)
- [ ] Update profile
- [ ] Restart server
- [ ] Check profile - Should have saved data

## 🐛 Troubleshooting

### Database Issues

**Error: "Database not configured"**
- Check `NEON_DB_URL` in `.env`
- Verify connection string format
- Test connection: `python init_db.py`

**Error: "Table 'users' doesn't exist"**
- Run: `python init_db.py`
- Check database permissions

### Qdrant Issues

**Error: "Could not connect to Qdrant"**
- Check `QDRANT_URL` or `QDRANT_HOST`/`QDRANT_PORT`
- Verify API key if using Qdrant Cloud
- Test: `python ingest_docs.py`

**Chatbot not finding context**
- Run: `python ingest_docs.py`
- Check collection name matches
- Verify embeddings were created

### OpenAI Issues

**Error: "OpenAI API quota exceeded"**
- Check billing at https://platform.openai.com/account/billing
- Verify API key is valid
- Check usage limits

**Error: "Invalid API key"**
- Verify `OPENAI_API_KEY` in `.env`
- Check key format (should start with `sk-`)
- Regenerate key if needed

### Frontend Issues

**CORS Error**
- Check `CORS_ORIGINS` in backend `.env`
- Add frontend URL to allowed origins
- Restart backend server

**Authentication not working**
- Check backend is running on port 8000
- Verify API endpoints in browser console
- Check localStorage for `user_id` and `token`

## 📊 Feature Status

| Feature | Status | Notes |
|---------|--------|-------|
| Authentication | ✅ Ready | Requires Neon DB |
| Database | ✅ Ready | Run `init_db.py` first |
| Profile | ✅ Ready | Loads from DB |
| Personalization | ✅ Ready | Uses DB profile |
| Translation | ✅ Ready | Requires OpenAI API |
| Markdown Ingestion | ✅ Ready | Run `ingest_docs.py` |
| Text Selection | ✅ Ready | Works on docs pages |
| Chatbot | ✅ Ready | Requires Qdrant + OpenAI |

## 🎯 Quick Start Commands

```bash
# 1. Setup environment
cd backend
# Edit .env file with your credentials

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python init_db.py

# 4. Ingest documents
python ingest_docs.py

# 5. Start backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 6. Start frontend (new terminal)
cd my-ai-book
npm start
```

## ✅ All Set!

Once all steps are complete:
1. ✅ Backend running on `http://localhost:8000`
2. ✅ Frontend running on `http://localhost:3000`
3. ✅ Database initialized
4. ✅ Documents ingested into Qdrant
5. ✅ All features ready to use!

**Test the complete flow:**
1. Sign up for an account
2. Update your profile
3. Browse docs pages
4. Select text and ask questions
5. Use chatbot for queries
6. Try translation feature
7. Test personalization

🎉 **Everything should be working perfectly!**

