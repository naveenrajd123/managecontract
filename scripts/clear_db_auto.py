"""
Quick script to clear database without user confirmation
"""
import asyncio
import sys
from sqlalchemy import delete
from src.database import Contract, AsyncSessionLocal, init_db

async def clear_all_contracts():
    try:
        # Initialize database
        await init_db()
        
        # Get session
        async with AsyncSessionLocal() as session:
            # Count existing contracts
            from sqlalchemy import select, func
            result = await session.execute(select(func.count(Contract.id)))
            count = result.scalar()
            
            print(f"[INFO] Found {count} contracts in database")
            
            if count == 0:
                print("[OK] Database is already empty!")
                return
            
            # Delete all contracts
            print(f"[PROCESSING] Deleting {count} contracts...")
            await session.execute(delete(Contract))
            await session.commit()
            
            print(f"[OK] Successfully deleted {count} contracts!")
            
    except Exception as e:
        print(f"[ERROR] Error clearing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(clear_all_contracts())
