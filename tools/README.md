# Utility Tools

This directory contains utility scripts for debugging and maintenance.

## Available Tools

### 1. test_system.py
**Purpose**: Comprehensive system health check

**Usage**:
```bash
python tools/test_system.py
```

**Checks**:
- Database connectivity and contents
- Required files and directories
- Environment configuration (API keys)
- Python package dependencies
- Upload log status

**Output**: Pass/Fail report for each component

---

### 2. check_db.py
**Purpose**: Quick database inspection

**Usage**:
```bash
python tools/check_db.py
```

**Shows**:
- Total contract count
- Sample contracts (first 10)
- Status breakdown (active, expired, etc.)
- Risk level distribution

**Use when**: You want to quickly see what's in the database without starting the server

---

## Quick Commands

```bash
# Full system health check
python tools/test_system.py

# Quick database check
python tools/check_db.py

# View upload history
type upload_log.txt

# Start the server
python -m src.main
```

## When to Use These Tools

### Before Starting Server
Run `test_system.py` to verify everything is configured correctly

### After Bulk Uploads
Run `check_db.py` to verify contracts were added successfully

### When Debugging Issues
1. Run `test_system.py` to identify problems
2. Run `check_db.py` to verify database state
3. Check `upload_log.txt` for upload history
4. Check server terminal for error messages

### When Friend Says "I See Zero Contracts"
1. Verify server is running
2. Run `check_db.py` to check actual database contents
3. Have them check browser console (F12) for errors
4. Test API directly: http://localhost:8000/api/dashboard/stats
