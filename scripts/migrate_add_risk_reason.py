"""
Migration script to add risk_reason column to contracts table
"""
import sqlite3
import asyncio

async def migrate():
    # Connect to the database
    conn = sqlite3.connect('contracts.db')
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(contracts)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'risk_reason' not in columns:
            print("[INFO] Adding risk_reason column to contracts table...")
            cursor.execute("ALTER TABLE contracts ADD COLUMN risk_reason TEXT")
            conn.commit()
            print("[SUCCESS] Column added successfully!")
        else:
            print("[INFO] Column risk_reason already exists")
            
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    asyncio.run(migrate())
