#!/usr/bin/env python
"""
System Health Check Script
Run this to verify the Contract Management System is working correctly
"""
import sqlite3
import os
import sys
from datetime import datetime

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_database():
    """Check database connectivity and contents"""
    print_header("1. DATABASE CHECK")
    
    if not os.path.exists('contracts.db'):
        print("[ERROR] contracts.db file not found!")
        print("        The database should be created when you first run the server.")
        return False
    
    try:
        conn = sqlite3.connect('contracts.db')
        cursor = conn.cursor()
        
        # Check if contracts table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contracts'")
        if not cursor.fetchone():
            print("[ERROR] contracts table not found in database!")
            return False
        
        # Get contract count
        cursor.execute('SELECT COUNT(*) FROM contracts')
        total = cursor.fetchone()[0]
        print(f"[OK] Database connected successfully")
        print(f"[INFO] Total contracts: {total}")
        
        if total > 0:
            # Show breakdown
            cursor.execute('SELECT status, COUNT(*) FROM contracts GROUP BY status')
            print(f"\n[INFO] Status breakdown:")
            for row in cursor.fetchall():
                print(f"       - {row[0]}: {row[1]}")
        else:
            print("[WARNING] No contracts in database yet")
            print("          Upload some contracts to get started!")
        
        conn.close()
        return True
    
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        return False

def check_files():
    """Check required files and directories"""
    print_header("2. FILE SYSTEM CHECK")
    
    checks = {
        'static/index.html': 'Frontend HTML file',
        'static/app.js': 'Frontend JavaScript',
        'static/styles.css': 'Frontend CSS',
        'src/main.py': 'Backend API',
        'src/database.py': 'Database models',
        'src/rag_system.py': 'AI/RAG system',
        'src/config.py': 'Configuration',
        '.env': 'Environment variables (API keys)',
        'uploads/': 'Uploads directory',
    }
    
    all_ok = True
    for file_path, description in checks.items():
        if os.path.exists(file_path):
            print(f"[OK] {description:30} -> {file_path}")
        else:
            print(f"[MISSING] {description:30} -> {file_path}")
            all_ok = False
    
    return all_ok

def check_env():
    """Check environment configuration"""
    print_header("3. ENVIRONMENT CHECK")
    
    if not os.path.exists('.env'):
        print("[ERROR] .env file not found!")
        print("        Create .env file with: GEMINI_API_KEY=your_key_here")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
    
    if 'GEMINI_API_KEY' in content:
        print("[OK] GEMINI_API_KEY found in .env")
        # Check if it's not empty
        for line in content.split('\n'):
            if line.startswith('GEMINI_API_KEY='):
                value = line.split('=', 1)[1].strip()
                if value and value != 'your_key_here':
                    print("[OK] API key appears to be set")
                    return True
                else:
                    print("[ERROR] API key is empty or placeholder")
                    return False
    else:
        print("[ERROR] GEMINI_API_KEY not found in .env")
        return False

def check_upload_log():
    """Check upload log for recent activity"""
    print_header("4. UPLOAD LOG CHECK")
    
    if not os.path.exists('upload_log.txt'):
        print("[INFO] No upload log found yet")
        print("       Log will be created after first upload")
        return True
    
    try:
        with open('upload_log.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) <= 1:  # Just header
            print("[INFO] No uploads recorded yet")
            return True
        
        print(f"[INFO] Found {len(lines)-1} upload attempts")
        
        # Count by status
        statuses = {}
        for line in lines[1:]:  # Skip header
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    status = parts[2].strip()
                    statuses[status] = statuses.get(status, 0) + 1
        
        print(f"\n[INFO] Upload statistics:")
        for status, count in statuses.items():
            print(f"       - {status}: {count}")
        
        # Show last 5 attempts
        print(f"\n[INFO] Last 5 upload attempts:")
        for line in lines[-5:]:
            if '|' in line:
                print(f"       {line.strip()}")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to read upload log: {e}")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    print_header("5. PYTHON PACKAGES CHECK")
    
    required = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'sqlalchemy': 'sqlalchemy',
        'aiosqlite': 'aiosqlite',
        'google-generativeai': 'google.generativeai',
        'PyPDF2': 'PyPDF2',
        'python-multipart': 'multipart',
        'pydantic': 'pydantic',
    }
    
    all_ok = True
    for package_name, import_name in required.items():
        try:
            __import__(import_name)
            print(f"[OK] {package_name}")
        except ImportError:
            print(f"[MISSING] {package_name}")
            all_ok = False
    
    if not all_ok:
        print("\n[ERROR] Some packages are missing!")
        print("        Run: pip install -r requirements.txt")
    
    return all_ok

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("  CONTRACT MANAGEMENT SYSTEM - HEALTH CHECK")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*60)
    
    results = {
        'Database': check_database(),
        'Files': check_files(),
        'Environment': check_env(),
        'Python Packages': check_python_packages(),
        'Upload Log': check_upload_log(),
    }
    
    print_header("SUMMARY")
    
    all_passed = True
    for check, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {check}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("  [SUCCESS] All checks passed!")
        print("  Your system is ready to use.")
        print("\n  To start the server, run:")
        print("  python -m src.main")
    else:
        print("  [WARNING] Some checks failed!")
        print("  Please fix the issues above before running the server.")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
