"""
Backfill risk reasons for existing contracts
This script re-analyzes all contracts that don't have risk reasons
"""
import asyncio
import sqlite3
import os
from rag_system import rag_system

async def backfill_risk_reasons():
    """Analyze all contracts without risk reasons and add them."""
    
    # Connect to database
    conn = sqlite3.connect('contracts.db')
    cursor = conn.cursor()
    
    # Find contracts without risk reasons
    cursor.execute("""
        SELECT id, contract_number, file_path, risk_level 
        FROM contracts 
        WHERE risk_reason IS NULL AND file_path IS NOT NULL
    """)
    
    contracts = cursor.fetchall()
    
    if not contracts:
        print("[INFO] All contracts already have risk reasons!")
        conn.close()
        return
    
    print(f"[INFO] Found {len(contracts)} contracts without risk reasons")
    print("[INFO] Starting AI analysis (this may take a few minutes)...\n")
    
    success_count = 0
    error_count = 0
    
    for contract_id, contract_number, file_path, risk_level in contracts:
        try:
            print(f"[INFO] Analyzing contract {contract_number} (ID: {contract_id})...")
            
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"[WARNING] File not found: {file_path}")
                error_count += 1
                continue
            
            # Read contract text
            contract_text = ""
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == ".txt":
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    contract_text = f.read()
            elif file_extension == ".pdf":
                try:
                    from PyPDF2 import PdfReader
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        contract_text += page.extract_text()
                except Exception as e:
                    print(f"[ERROR] Failed to read PDF: {e}")
                    error_count += 1
                    continue
            
            if not contract_text or len(contract_text) < 100:
                print(f"[WARNING] Contract text too short or empty")
                error_count += 1
                continue
            
            # Assess risk with AI
            risk_assessment = await rag_system.assess_risk_level(contract_text)
            risk_reason = risk_assessment.get("risk_reason", "Risk level determined by contract analysis")
            
            # Update database
            cursor.execute("""
                UPDATE contracts 
                SET risk_reason = ? 
                WHERE id = ?
            """, (risk_reason, contract_id))
            conn.commit()
            
            print(f"[SUCCESS] {contract_number}: {risk_reason[:80]}...")
            success_count += 1
            
        except Exception as e:
            print(f"[ERROR] Failed to analyze contract {contract_number}: {e}")
            error_count += 1
            continue
    
    conn.close()
    
    print(f"\n[COMPLETE] Backfill finished!")
    print(f"[SUCCESS] {success_count} contracts updated")
    print(f"[ERROR] {error_count} contracts failed")

if __name__ == "__main__":
    asyncio.run(backfill_risk_reasons())
