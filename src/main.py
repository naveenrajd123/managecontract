"""
Main FastAPI Application
This is the heart of the backend - it handles all API requests.

What is an API?
- API = Application Programming Interface
- It's like a waiter in a restaurant: takes requests, brings back responses
- Our frontend (webpage) will talk to this API
"""

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime, timedelta
import os
import json
import traceback

# Import our custom modules
from src.database import init_db, get_db, Contract
from src.rag_system import rag_system
from src.early_warning import early_warning_system
from src.config import settings
from src.schemas import ContractCreate, ContractResponse, ContractUpdate, QuestionRequest

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Contract Management with Early Warning System",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    await init_db()
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
    
    # Load all existing contracts into RAG system
    print("[INFO] Loading existing contracts into RAG system...")
    async for db in get_db():
        try:
            # Query all contracts from database
            result = await db.execute(select(Contract))
            contracts = result.scalars().all()
            
            print(f"[INFO] Found {len(contracts)} contracts in database")
            
            # Load each contract into RAG system
            for contract in contracts:
                if contract.file_path and os.path.exists(contract.file_path):
                    await rag_system.load_contract_from_file(
                        contract_id=contract.id,
                        file_path=contract.file_path,
                        contract_metadata={
                            "name": contract.contract_name,
                            "number": contract.contract_number,
                            "party_a": contract.party_a,
                            "party_b": contract.party_b
                        }
                    )
                else:
                    print(f"[WARNING] Contract {contract.id} file not found: {contract.file_path}")
            
            print(f"[SUCCESS] RAG system initialized with {len(rag_system.contracts_storage)} contracts")
            break  # Only need one db session
        except Exception as e:
            print(f"[ERROR] Failed to load contracts into RAG system: {e}")
            import traceback
            traceback.print_exc()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main dashboard HTML page."""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except Exception:
        return HTMLResponse(content="""
        <html>
            <body>
                <h1>Contract Management System</h1>
                <p>API is running! Frontend is being set up...</p>
                <p>Visit <a href="/docs">/docs</a> for API documentation</p>
            </body>
        </html>
        """, status_code=200)


# Mount static files AFTER defining the root route
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# ============================================================================
# CONTRACT ENDPOINTS
# ============================================================================

@app.post("/api/contracts", response_model=ContractResponse)
async def create_contract(
    contract: ContractCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new contract (without file upload).
    
    This is useful for manually entering contract details.
    """
    # Create database record
    db_contract = Contract(
        contract_name=contract.contract_name,
        contract_number=contract.contract_number,
        party_a=contract.party_a,
        party_b=contract.party_b,
        start_date=contract.start_date,
        end_date=contract.end_date,
        status=contract.status or "active",
        contract_value=contract.contract_value,
        currency=contract.currency,
        risk_level=contract.risk_level or "low"
    )
    
    db.add(db_contract)
    await db.commit()
    await db.refresh(db_contract)
    
    return db_contract


@app.get("/api/contracts", response_model=List[ContractResponse])
async def get_contracts(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all contracts (with optional filtering).
    
    Query Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return
    - status: Filter by status (active, expired, etc.)
    """
    query = select(Contract)
    
    if status:
        query = query.where(Contract.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Contract.created_at.desc())
    
    result = await db.execute(query)
    contracts = result.scalars().all()
    
    return contracts


@app.get("/api/contracts/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific contract by ID.
    """
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    return contract


@app.put("/api/contracts/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: int,
    contract_update: ContractUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing contract.
    """
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Update fields
    update_data = contract_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contract, field, value)
    
    contract.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(contract)
    
    return contract


@app.delete("/api/contracts/{contract_id}")
async def delete_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a contract.
    """
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    await db.delete(contract)
    await db.commit()
    
    return {"message": "Contract deleted successfully"}


@app.post("/api/contracts/{contract_id}/reanalyze")
async def reanalyze_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Re-analyze a contract to update its risk reason.
    Useful for contracts uploaded before the risk_reason feature was added.
    """
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    if not contract.file_path or not os.path.exists(contract.file_path):
        raise HTTPException(status_code=400, detail="Contract file not found")
    
    try:
        # Read contract text
        contract_text = ""
        file_extension = os.path.splitext(contract.file_path)[1].lower()
        
        if file_extension == ".txt":
            with open(contract.file_path, "r", encoding="utf-8", errors="ignore") as f:
                contract_text = f.read()
        elif file_extension == ".pdf":
            from PyPDF2 import PdfReader
            reader = PdfReader(contract.file_path)
            for page in reader.pages:
                contract_text += page.extract_text()
        
        if not contract_text or len(contract_text) < 100:
            raise HTTPException(status_code=400, detail="Contract text too short or empty")
        
        # Assess risk with AI
        risk_assessment = await rag_system.assess_risk_level(contract_text)
        risk_reason = risk_assessment.get("risk_reason", "Risk level determined by contract analysis")
        
        # Update contract
        contract.risk_reason = risk_reason
        contract.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(contract)
        
        return {
            "message": "Contract re-analyzed successfully",
            "risk_level": contract.risk_level,
            "risk_reason": risk_reason
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to re-analyze contract: {str(e)}")


@app.post("/api/contracts/reanalyze-all")
async def reanalyze_all_contracts(db: AsyncSession = Depends(get_db)):
    """
    Re-analyze all contracts that don't have risk reasons.
    This is a bulk operation for contracts uploaded before the risk_reason feature.
    """
    try:
        # Find all contracts without risk reasons
        result = await db.execute(
            select(Contract).where(
                Contract.risk_reason.is_(None),
                Contract.file_path.isnot(None)
            )
        )
        contracts = result.scalars().all()
        
        if not contracts:
            return {
                "message": "All contracts already have risk reasons!",
                "total": 0,
                "success": 0,
                "failed": 0,
                "results": []
            }
        
        results = []
        success_count = 0
        failed_count = 0
        
        for contract in contracts:
            try:
                # Check if file exists
                if not os.path.exists(contract.file_path):
                    results.append({
                        "contract_id": contract.id,
                        "contract_number": contract.contract_number,
                        "status": "error",
                        "message": "File not found"
                    })
                    failed_count += 1
                    continue
                
                # Read contract text
                contract_text = ""
                file_extension = os.path.splitext(contract.file_path)[1].lower()
                
                if file_extension == ".txt":
                    with open(contract.file_path, "r", encoding="utf-8", errors="ignore") as f:
                        contract_text = f.read()
                elif file_extension == ".pdf":
                    from PyPDF2 import PdfReader
                    reader = PdfReader(contract.file_path)
                    for page in reader.pages:
                        contract_text += page.extract_text()
                
                if not contract_text or len(contract_text) < 100:
                    results.append({
                        "contract_id": contract.id,
                        "contract_number": contract.contract_number,
                        "status": "error",
                        "message": "Contract text too short"
                    })
                    failed_count += 1
                    continue
                
                # Assess risk with AI
                risk_assessment = await rag_system.assess_risk_level(contract_text)
                risk_reason = risk_assessment.get("risk_reason", "Risk level determined by contract analysis")
                
                # Update contract
                contract.risk_reason = risk_reason
                contract.updated_at = datetime.utcnow()
                
                results.append({
                    "contract_id": contract.id,
                    "contract_number": contract.contract_number,
                    "status": "success",
                    "risk_reason": risk_reason
                })
                success_count += 1
                
            except Exception as e:
                results.append({
                    "contract_id": contract.id,
                    "contract_number": contract.contract_number,
                    "status": "error",
                    "message": str(e)
                })
                failed_count += 1
        
        # Commit all changes
        await db.commit()
        
        return {
            "message": f"Bulk re-analysis completed: {success_count} succeeded, {failed_count} failed",
            "total": len(contracts),
            "success": success_count,
            "failed": failed_count,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to re-analyze contracts: {str(e)}")


# ============================================================================
# FILE UPLOAD ENDPOINT
# ============================================================================

def log_upload_attempt(filename: str, status: str, message: str):
    """Log upload attempts to file for debugging"""
    try:
        with open("upload_log.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} | {filename} | {status} | {message}\n")
    except:
        pass  # Don't let logging errors break uploads


@app.post("/api/contracts/upload")
async def upload_contract(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a contract file and automatically extract all details using AI.
    
    This endpoint:
    1. Saves the file
    2. Extracts text from PDF/TXT
    3. Uses AI to extract metadata (name, parties, dates, value)
    4. Generates summary and assesses risk
    5. Stores everything in database
    """
    try:
        print(f"\n[UPLOAD] Starting upload for file: {file.filename}")
        log_upload_attempt(file.filename, "STARTED", "Upload initiated")
        
        # Validate file type
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            print(f"[UPLOAD ERROR] Invalid file type: {file_extension}")
            log_upload_attempt(file.filename, "REJECTED", f"Invalid file type: {file_extension}")
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_extension} not allowed. Use PDF or TXT files."
            )
    
    # Generate temporary filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_filename = f"temp_{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIRECTORY, temp_filename)
    
    print(f"[UPLOAD] Saving file to: {file_path}")
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        print(f"[UPLOAD] File saved successfully, size: {len(content)} bytes")
    except Exception as e:
        print(f"[UPLOAD ERROR] Failed to save file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Extract text from file
    print(f"[UPLOAD] Extracting text from {file_extension} file...")
    contract_text = ""
    if file_extension == ".txt":
        contract_text = content.decode("utf-8", errors="ignore")
        print(f"[UPLOAD] Extracted {len(contract_text)} characters from TXT")
    elif file_extension == ".pdf":
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            print(f"[UPLOAD] PDF has {len(reader.pages)} pages")
            for page in reader.pages:
                contract_text += page.extract_text()
            print(f"[UPLOAD] Extracted {len(contract_text)} characters from PDF")
        except Exception as e:
            print(f"[UPLOAD ERROR] Failed to read PDF: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to read PDF: {str(e)}"
            )
    
    if not contract_text or len(contract_text) < 100:
        print(f"[UPLOAD ERROR] Contract text too short: {len(contract_text)} characters")
        raise HTTPException(
            status_code=400,
            detail="Contract file appears empty or could not be read"
        )
    
    # Step 1: Extract metadata using AI
    print(f"[UPLOAD] Step 1/4: Extracting metadata with AI...")
    try:
        metadata = await rag_system.extract_contract_metadata(contract_text)
        print(f"[UPLOAD] Metadata extracted: {metadata.get('contract_number', 'N/A')}")
    except Exception as e:
        print(f"[UPLOAD ERROR] Failed to extract metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI metadata extraction failed: {str(e)}")
    
    # Step 2: Generate summary
    print(f"[UPLOAD] Step 2/4: Generating summary with AI...")
    try:
        summary = await rag_system.generate_contract_summary(contract_text)
        print(f"[UPLOAD] Summary generated ({len(summary)} chars)")
    except Exception as e:
        print(f"[UPLOAD ERROR] Failed to generate summary: {str(e)}")
        summary = "Summary generation failed"
    
    # Step 3: Extract key clauses
    print(f"[UPLOAD] Step 3/4: Extracting key clauses with AI...")
    try:
        key_clauses = await rag_system.extract_key_clauses(contract_text)
        print(f"[UPLOAD] Key clauses extracted")
    except Exception as e:
        print(f"[UPLOAD ERROR] Failed to extract key clauses: {str(e)}")
        key_clauses = {}
    
    # Step 4: Assess risk
    print(f"[UPLOAD] Step 4/4: Assessing risk level with AI...")
    try:
        risk_assessment = await rag_system.assess_risk_level(contract_text)
        print(f"[UPLOAD] Risk assessment: {risk_assessment.get('risk_level', 'unknown')}")
    except Exception as e:
        print(f"[UPLOAD ERROR] Failed to assess risk: {str(e)}")
        risk_assessment = {"risk_level": "medium", "risk_reason": "Risk assessment failed"}
    
    # Parse dates
    from dateutil import parser as date_parser
    try:
        start_date = date_parser.parse(metadata['start_date']) if metadata.get('start_date') else datetime.now()
    except:
        start_date = datetime.now()
    
    try:
        end_date = date_parser.parse(metadata['end_date']) if metadata.get('end_date') else datetime.now() + timedelta(days=365)
    except:
        end_date = datetime.now() + timedelta(days=365)
    
    # Determine status based on dates
    current_date = datetime.now()
    if end_date < current_date:
        status = "expired"
    elif start_date > current_date:
        status = "pending"
    else:
        status = "active"
    
    # Rename file with contract number
    contract_number = metadata.get('contract_number', f"CNT-{timestamp}")
    final_filename = f"{contract_number}_{file.filename}"
    final_path = os.path.join(settings.UPLOAD_DIRECTORY, final_filename)
    
    # Rename file
    if os.path.exists(final_path):
        os.remove(final_path)
    os.rename(file_path, final_path)
    
    # Create database record
    db_contract = Contract(
        contract_name=metadata.get('contract_name', 'Untitled Contract'),
        contract_number=contract_number,
        party_a=metadata.get('party_a', 'Unknown'),
        party_b=metadata.get('party_b', 'Unknown'),
        start_date=start_date,
        end_date=end_date,
        contract_value=metadata.get('contract_value'),
        currency=metadata.get('currency', 'USD'),
        file_path=final_path,
        file_type=file_extension,
        summary=summary,
        key_clauses=json.dumps(key_clauses),
        risk_level=risk_assessment["risk_level"],
        risk_reason=risk_assessment.get("risk_reason", "Risk level determined by contract analysis"),
        status=status
    )
    
    print(f"[UPLOAD] Saving contract to database...")
    db.add(db_contract)
    try:
        await db.commit()
        await db.refresh(db_contract)
        print(f"[UPLOAD SUCCESS] Contract saved with ID: {db_contract.id}")
    except Exception as e:
        await db.rollback()
        print(f"[UPLOAD ERROR] Database error: {str(e)}")
        if "UNIQUE constraint failed" in str(e) or "unique" in str(e).lower():
            log_upload_attempt(file.filename, "DUPLICATE", f"Contract {contract_number} already exists")
            raise HTTPException(
                status_code=400,
                detail=f"Contract number {contract_number} already exists in database. Please upload a different contract."
            )
        else:
            log_upload_attempt(file.filename, "DB_ERROR", f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    # Add to vector database for RAG
    print(f"[UPLOAD] Adding contract to RAG vector database...")
    try:
        await rag_system.add_contract_to_vectordb(
            contract_id=db_contract.id,
            contract_text=contract_text,
            contract_metadata={
                "name": metadata.get('contract_name'),
                "number": contract_number,
                "party_a": metadata.get('party_a'),
                "party_b": metadata.get('party_b')
            }
        )
        print(f"[UPLOAD] Successfully added to RAG system")
    except Exception as e:
        print(f"[UPLOAD WARNING] Failed to add to RAG system: {str(e)}")
        # Don't fail the upload if RAG indexing fails
    
        print(f"[UPLOAD COMPLETE] Contract {contract_number} uploaded successfully!\n")
        log_upload_attempt(file.filename, "SUCCESS", f"Contract {contract_number} uploaded with ID {db_contract.id}")
        
        return {
            "message": "Contract uploaded and processed successfully",
            "id": db_contract.id,
            "contract_id": db_contract.id,
            "contract_number": contract_number,
            "contract_name": metadata.get('contract_name'),
            "party_a": metadata.get('party_a'),
            "party_b": metadata.get('party_b'),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "status": status,
            "risk_level": risk_assessment["risk_level"],
            "risk_reason": risk_assessment.get("risk_reason", ""),
            "summary": summary
        }
    
    except HTTPException:
        # Re-raise HTTP exceptions (already logged and handled)
        raise
    except Exception as e:
        # Catch any unexpected errors
        error_msg = f"Unexpected error during upload: {str(e)}"
        print(f"[UPLOAD CRITICAL ERROR] {error_msg}")
        print(f"[UPLOAD TRACEBACK] {traceback.format_exc()}")
        log_upload_attempt(file.filename, "FAILED", error_msg)
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}. Check server logs for details."
        )


# ============================================================================
# RAG / AI QUERY ENDPOINTS
# ============================================================================

@app.post("/api/contracts/ask")
async def ask_question(
    question_data: QuestionRequest
):
    """
    Ask a question about contracts using RAG.
    
    Example questions:
    - "What are the payment terms in contract #12345?"
    - "Which contracts have termination clauses?"
    - "Summarize the renewal terms"
    """
    answer = await rag_system.answer_question(
        question=question_data.question,
        contract_id=question_data.contract_id
    )
    
    return {"question": question_data.question, "answer": answer}


# ============================================================================
# EARLY WARNING ENDPOINTS
# ============================================================================

@app.get("/api/warnings")
async def get_warnings(db: AsyncSession = Depends(get_db)):
    """
    Get all active warnings and alerts.
    
    Returns warnings for:
    - Contracts expiring soon
    - Expired contracts
    - High-risk contracts
    """
    warnings = await early_warning_system.get_all_warnings(db)
    stats = early_warning_system.get_dashboard_stats(warnings)
    
    return {
        "warnings": warnings,
        "stats": stats
    }


@app.get("/api/warnings/{contract_id}")
async def get_contract_warnings(
    contract_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get warnings for a specific contract.
    """
    warnings = await early_warning_system.get_contract_warnings(db, contract_id)
    return {"contract_id": contract_id, "warnings": warnings}


# ============================================================================
# DASHBOARD STATS ENDPOINT
# ============================================================================

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """
    Get statistics for the dashboard.
    
    Returns:
    - Total contracts
    - Active contracts
    - Expired contracts
    - Renewed contracts
    - Pending contracts
    - Total contract value
    - Risk distribution
    """
    # Total contracts
    total_result = await db.execute(select(func.count(Contract.id)))
    total_contracts = total_result.scalar()
    
    # Active contracts
    active_result = await db.execute(
        select(func.count(Contract.id)).where(Contract.status == "active")
    )
    active_contracts = active_result.scalar()
    
    # Expired contracts
    expired_result = await db.execute(
        select(func.count(Contract.id)).where(Contract.status == "expired")
    )
    expired_contracts = expired_result.scalar()
    
    # Renewed contracts
    renewed_result = await db.execute(
        select(func.count(Contract.id)).where(Contract.status == "renewed")
    )
    renewed_contracts = renewed_result.scalar()
    
    # Pending contracts
    pending_result = await db.execute(
        select(func.count(Contract.id)).where(Contract.status == "pending")
    )
    pending_contracts = pending_result.scalar()
    
    # Total value
    value_result = await db.execute(
        select(func.sum(Contract.contract_value)).where(Contract.status == "active")
    )
    total_value = value_result.scalar() or 0
    
    # Risk distribution
    risk_results = await db.execute(
        select(Contract.risk_level, func.count(Contract.id))
        .where(Contract.status == "active")
        .group_by(Contract.risk_level)
    )
    risk_distribution = {row[0]: row[1] for row in risk_results}
    
    return {
        "total_contracts": total_contracts,
        "active_contracts": active_contracts,
        "expired_contracts": expired_contracts,
        "renewed_contracts": renewed_contracts,
        "pending_contracts": pending_contracts,
        "total_value": float(total_value),
        "risk_distribution": risk_distribution
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """
    Check if the API is running.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
