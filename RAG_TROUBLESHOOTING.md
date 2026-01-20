# RAG System Troubleshooting Guide

## Problem: "I couldn't find relevant information in the contracts"

### What's Happening?
Your Contract Management System uses an **in-memory RAG (Retrieval Augmented Generation) system**. This means:

- When contracts are uploaded, they're stored in:
  1. ✅ Database (persistent)
  2. ✅ File system (persistent)
  3. ✅ RAG memory (IN-MEMORY - cleared on restart)

- When the server restarts (like on Render deployments), the RAG memory is cleared
- The system should automatically reload contracts from files during startup, but if this fails, the AI won't be able to access contract content

### Quick Fix (Use the UI)

1. Go to the **"Ask AI"** tab
2. Click the **"🔍 Check AI System Status"** button
3. If it shows a mismatch (e.g., "Database has 120 contracts but RAG has 0"):
   - A red warning banner will appear
   - Click **"🔄 Reload Contracts into AI Memory"**
   - Wait for the reload to complete
4. Try asking your question again!

### Manual Fix (Using API)

If you prefer to use the API directly:

1. **Check RAG Status:**
   ```bash
   curl https://your-app.onrender.com/api/debug/rag-status
   ```

2. **Reload RAG System:**
   ```bash
   curl -X POST https://your-app.onrender.com/api/debug/reload-rag
   ```

### Why Does This Happen?

On Render's free tier (and some paid tiers), services may:
- Restart periodically
- Go to sleep after inactivity
- Restart during deployments

Each restart clears the in-memory RAG storage. The startup script should reload contracts, but if:
- Files are missing
- File paths are incorrect
- Startup fails silently
- There's a timeout during startup

...the RAG system will be empty.

### Permanent Solution Options

#### Option 1: Automatic Reload on First Query (Recommended)
Modify the `answer_question` function to auto-reload if RAG is empty:

```python
async def answer_question(self, question: str, contract_id: int = None) -> str:
    # Auto-reload if RAG is empty
    if not self.contracts_storage and contract_id:
        print("[WARNING] RAG storage empty, attempting auto-reload...")
        # Trigger reload logic here
    
    # Rest of the function...
```

#### Option 2: Use a Persistent Vector Database
Instead of in-memory storage, use a persistent vector database like:
- **ChromaDB with persistent storage** (currently not used due to Python 3.14 compatibility)
- **Pinecone** (cloud-based, free tier available)
- **Qdrant** (can run in Docker or cloud)
- **Weaviate** (self-hosted or cloud)

#### Option 3: Scheduled Health Checks
Add a cron job or scheduled task that:
- Checks RAG status every 5 minutes
- Auto-reloads if empty
- Sends alerts if reload fails

### Current Status

✅ **Fixed in this update:**
- Added `/api/debug/rag-status` endpoint to check RAG health
- Added `/api/debug/reload-rag` endpoint to manually reload contracts
- Added UI buttons in the "Ask AI" tab for easy diagnostics
- Added automatic warning banner when AI can't find contracts

### Testing Your Fix

After deploying the update:

1. Open your app on Render
2. Go to "Ask AI" tab
3. Click "Check AI System Status"
4. If needed, click "Reload Contracts"
5. Try your question: "Summarize this contract"
6. Should work now! ✅

### For Developers

The RAG system code is in `src/rag_system.py`:
- `contracts_storage = {}` - This is the in-memory dict that gets cleared
- `load_contract_from_file()` - Called during startup to reload contracts
- `add_contract_to_vectordb()` - Called when uploading new contracts

The startup reload happens in `src/main.py`:
```python
@app.on_event("startup")
async def startup_event():
    # Loads all contracts from database into RAG
```

### Common Issues

1. **Files not found**: Contract files might not have uploaded correctly
2. **Wrong file paths**: Check `uploads/` directory exists and has proper permissions
3. **Database out of sync**: Database has contracts but files are missing
4. **Startup timeout**: Too many contracts to load within startup window

Check the Render logs for:
```
[INFO] Loading existing contracts into RAG system...
[INFO] Found X contracts in database
[SUCCESS] RAG system initialized with X contracts
```

If you see errors or mismatches, use the reload endpoint!
