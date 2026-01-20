# 🔧 Render Deployment Fix Guide

## ❌ The Problem You're Seeing

**Error:** "Database has 62 contracts but RAG has 0"  
**When Reloading:** "Loaded: 0 contracts, Failed: 62 contracts"

### Why This Happens

1. **Ephemeral Storage Issue:**
   - Render's default storage is **ephemeral** (temporary)
   - Files uploaded locally don't exist on Render
   - Database records exist, but the actual PDF/TXT files are missing
   - Every deployment wipes the file system

2. **What You Had:**
   ```
   Local Machine:
   ├── contracts.db (database with 62 records) ✅
   └── uploads/ (62 PDF/TXT files) ✅
   
   Render Production:
   ├── contracts.db (database with 62 records) ✅
   └── uploads/ (EMPTY - files lost!) ❌
   ```

---

## ✅ Solution: Persistent Disk Storage

I've updated your `render.yaml` to add **persistent disk storage** that survives deployments.

### What Changed:

```yaml
# NEW: Persistent disk configuration
disk:
  name: contract-data
  mountPath: /opt/render/project/src/data
  sizeGB: 1

# Updated paths to use persistent storage
DATABASE_URL: sqlite+aiosqlite:///./data/contracts.db
UPLOAD_DIRECTORY: ./data/uploads
```

---

## 🚀 Steps to Fix Your Production Deployment

### Step 1: Wait for Automatic Redeployment (5-10 minutes)

The push I just made will trigger automatic redeployment. Render will:
- ✅ Create a persistent disk (1GB)
- ✅ Mount it at `/opt/render/project/src/data`
- ✅ Redeploy with new configuration

**Check status:** https://dashboard.render.com

---

### Step 2: After Deployment Completes

#### Option A: Start Fresh (RECOMMENDED for Demo)

1. **Delete all contracts** using the "Delete Contracts" button in your dashboard
2. **Upload sample contracts** from your `demo_contracts2` folder
3. Files will now persist on the disk!

#### Option B: Keep Existing Database

Your 62 database records will remain, but:
- ❌ The files are still missing
- ❌ RAG won't work until you re-upload the files
- You'll need to upload all 62 files again

---

### Step 3: Verify It's Working

1. Go to your production URL
2. Upload a test contract
3. Check RAG status - should show: "Database has 1 contracts, RAG has 1"
4. Try asking AI questions - should work now!

---

## 📊 What This Costs

**Persistent Disk Pricing (Render):**
- 1GB disk: **$1/month**
- Totally worth it for file persistence!

---

## 🎯 Alternative Solutions (If You Don't Want Persistent Disk)

### Option 1: Use Cloud Storage (S3, Cloudflare R2)

**Benefits:**
- No persistent disk needed
- Cheaper for large files
- Better for production scale

**Requires:**
- Add boto3 to requirements.txt
- Store files in S3 instead of local disk
- Update upload logic

### Option 2: Database-Only (No Files)

**Store contract text directly in database:**
- Don't keep PDF files
- Extract text during upload
- Store text in database
- Delete uploaded file immediately

**Trade-offs:**
- ❌ Can't download original files
- ❌ Lose formatting/metadata
- ✅ No file storage needed
- ✅ Simpler deployment

---

## 🔍 How to Check Disk Status on Render

1. Go to https://dashboard.render.com
2. Select your `contract-management-system` service
3. Go to "Disks" tab
4. You should see `contract-data` (1GB)

---

## 📝 Updated File Structure (Production)

```
Render Production (After Fix):
├── /opt/render/project/src/
│   ├── main.py
│   ├── rag_system.py
│   └── data/  ← PERSISTENT DISK MOUNTED HERE
│       ├── contracts.db (survives deployments)
│       └── uploads/ (survives deployments)
│           ├── CNT-2024-001_contract.pdf
│           ├── CNT-2024-002_agreement.pdf
│           └── ... (all uploaded files persist!)
```

---

## ⚠️ Important Notes

### Database Migration Needed

Since we changed the database path from `./contracts.db` to `./data/contracts.db`:

**Option 1: Start Fresh (Easiest)**
- Let Render create a new empty database
- Upload contracts again
- Everything will work

**Option 2: Migrate Existing Data**
- SSH into Render
- Copy `./contracts.db` to `./data/contracts.db`
- Restart service

---

## 🐛 If You Still See Issues

### Issue: "Disk not found"

**Fix:**
1. Go to Render Dashboard → Your Service
2. Click "Disks" tab
3. Click "Add Disk"
4. Name: `contract-data`
5. Size: 1 GB
6. Mount path: `/opt/render/project/src/data`
7. Redeploy

### Issue: "Permission denied"

**Fix:** Render should auto-set permissions, but if not:
```bash
# In Render shell
chmod -R 755 /opt/render/project/src/data
```

### Issue: "RAG still has 0 contracts"

**Diagnose:**
1. Click "Check AI System Status" button
2. Check error logs
3. Verify files exist: `/opt/render/project/src/data/uploads/`

---

## 📊 Monitoring Your Deployment

### Check These Metrics:

1. **Disk Usage:**
   - Go to Render Dashboard → Disks
   - Monitor: Used space / 1GB
   - Alert when > 800MB

2. **RAG Status:**
   - Use "Check AI System Status" button
   - Should match: Database count = RAG count

3. **Upload Success Rate:**
   - Monitor upload logs
   - Check for file permission errors

---

## 🎓 For Your Interview

**You can now explain:**

> "Initially, I deployed on ephemeral storage which caused file persistence 
> issues. I solved it by adding a 1GB persistent disk mounted at a specific 
> path, ensuring uploaded contracts survive deployments. This is a common 
> production consideration when deploying to cloud platforms like Render, 
> AWS, or Azure - you need to distinguish between ephemeral compute and 
> persistent storage layers."

**Data Engineering Concepts:**
- Ephemeral vs persistent storage
- Stateful vs stateless applications
- Cloud storage architecture
- File system design for production

---

## ✅ Success Checklist

- [ ] Render redeployment completed
- [ ] Persistent disk created (1GB)
- [ ] Database at `/data/contracts.db`
- [ ] Upload directory at `/data/uploads`
- [ ] Uploaded test contract successfully
- [ ] RAG status shows matching counts
- [ ] AI Q&A works with uploaded contracts
- [ ] Files persist after redeployment

---

## 🚀 Next Steps

1. **Wait 10 minutes** for redeployment
2. **Check Render dashboard** for disk creation
3. **Test upload** a contract
4. **Verify RAG** is working
5. **Ready for interview!** 🎉

---

**Last Updated:** 2026-01-20  
**Status:** Fix deployed, waiting for Render redeployment
