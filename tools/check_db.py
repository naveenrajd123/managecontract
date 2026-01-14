#!/usr/bin/env python
"""Quick script to check the database contents"""
import sqlite3
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get database path from project root
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'contracts.db')

if not os.path.exists(db_path):
    print(f'\n[ERROR] Database not found at: {db_path}')
    print('[INFO] Make sure you are running this from the project root directory')
    sys.exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get total count
cursor.execute('SELECT COUNT(*) FROM contracts')
total = cursor.fetchone()[0]
print(f'\n[OK] Total contracts in database: {total}')

if total > 0:
    # Get sample contracts
    cursor.execute('SELECT id, contract_number, contract_name, status FROM contracts LIMIT 10')
    print('\n[SAMPLE] Sample contracts:')
    for row in cursor.fetchall():
        print(f'  - ID:{row[0]} | {row[1]}: {row[2]} | Status: {row[3]}')
    
    # Get status breakdown
    cursor.execute('SELECT status, COUNT(*) FROM contracts GROUP BY status')
    print('\n[STATUS] Status breakdown:')
    for row in cursor.fetchall():
        print(f'  - {row[0]}: {row[1]}')
    
    # Get risk breakdown
    cursor.execute('SELECT risk_level, COUNT(*) FROM contracts GROUP BY risk_level')
    print('\n[RISK] Risk level breakdown:')
    for row in cursor.fetchall():
        print(f'  - {row[0]}: {row[1]}')
else:
    print('\n[INFO] No contracts in database yet. Upload some contracts to get started!')

conn.close()
print()
