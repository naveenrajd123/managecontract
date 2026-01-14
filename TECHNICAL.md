# 🛠️ Technical Documentation

## Contract Management System - Technical Implementation Guide

---

## 📋 Table of Contents

1. [Technology Stack](#technology-stack)
2. [Architecture Overview](#architecture-overview)
3. [System Components](#system-components)
4. [Database Design](#database-design)
5. [API Endpoints](#api-endpoints)
6. [RAG Implementation](#rag-implementation)
7. [AI Integration](#ai-integration)
8. [Deployment](#deployment)
9. [Security](#security)
10. [Development Setup](#development-setup)

---

## 🎯 Technology Stack

### **Frontend**
- **HTML5** - Semantic markup with accessibility features
- **CSS3** - Custom styling with CSS Grid, Flexbox, CSS Variables
- **Vanilla JavaScript (ES6+)** - No frameworks, pure JavaScript for performance
- **Responsive Design** - Mobile-first approach with media queries

### **Backend**
- **Python 3.14** - Latest Python runtime
- **FastAPI** - High-performance async web framework
- **SQLAlchemy 2.0** - ORM with async support
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server for production

### **Database**
- **PostgreSQL 18** - Production database (Render deployment)
- **SQLite** - Local development database
- **asyncpg** - Async PostgreSQL driver
- **psycopg2-binary** - PostgreSQL adapter

### **AI & ML**
- **Google Gemini 2.5 Flash** - Large Language Model
- **google-generativeai** - Official Gemini Python SDK
- **RAG Pipeline** - Custom implementation for document retrieval

### **Deployment & DevOps**
- **Render** - Cloud platform (PaaS)
- **Git & GitHub** - Version control
- **Cursor.ai** - AI-powered IDE
- **Claude Sonnet 4.5** - AI assistant for development

---

## 🏗️ Architecture Overview

### **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Browser                          │
│                  (HTML + CSS + JavaScript)                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ HTTP/HTTPS
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                     FastAPI Server                           │
│                   (Python + Uvicorn)                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Contract   │  │  RAG System  │  │Early Warning │     │
│  │  Management  │  │              │  │    System    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────────┬─────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
    ┌─────────────┐  ┌──────────┐  ┌──────────┐
    │ PostgreSQL  │  │  Gemini  │  │  File    │
    │  Database   │  │   API    │  │ Storage  │
    └─────────────┘  └──────────┘  └──────────┘
```

### **Request Flow**

1. **Client Request** → User interaction in browser
2. **API Gateway** → FastAPI routes handle requests
3. **Business Logic** → Contract processing, RAG, warnings
4. **Data Layer** → Database queries and file operations
5. **AI Layer** → Gemini API for analysis
6. **Response** → JSON data back to client
7. **UI Update** → JavaScript updates DOM

---

## 🧩 System Components

### **1. Frontend Layer (`static/`)**

#### **index.html**
- Single-page application structure
- Tab-based navigation system
- Dashboard with real-time statistics
- Contract list with filtering
- Upload interface with drag & drop
- AI chat interface
- Responsive design

#### **styles.css**
- Modern gradient-based design
- CSS Grid for layouts
- CSS Variables for theming
- Animations and transitions
- Dark/light mode ready
- Mobile breakpoints

#### **app.js**
- API communication layer
- DOM manipulation
- Event handling
- Real-time updates
- File upload management
- Filtering and sorting logic

### **2. Backend Layer (`src/`)**

#### **main.py** - Application Core
```python
# FastAPI application
app = FastAPI(title="Contract Management System")

# Key endpoints:
- POST /api/contracts/upload        # Upload & analyze contracts
- GET  /api/contracts               # List contracts with filters
- GET  /api/contracts/{id}          # Get single contract
- DELETE /api/contracts/{id}        # Delete contract
- POST /api/contracts/ask           # RAG Q&A
- GET  /api/dashboard/stats         # Dashboard statistics
- GET  /api/warnings                # Early warning alerts
- POST /api/contracts/reanalyze-all # Bulk reanalysis
```

#### **database.py** - Data Layer
```python
# SQLAlchemy async setup
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine)

# Contract model with relationships
class Contract(Base):
    id: int
    contract_number: str (unique)
    contract_name: str
    party_a: str
    party_b: str
    start_date: datetime
    end_date: datetime
    status: str (active/expired/renewed/pending)
    contract_value: float
    currency: str
    risk_level: str (low/medium/high/critical)
    risk_reason: str
    file_path: str
    summary: str
    key_clauses: JSON
```

#### **rag_system.py** - RAG Implementation
```python
class ContractRAGSystem:
    # Core RAG functions
    - chunk_text()              # Split documents into chunks
    - add_contract_to_vectordb() # Store contract for retrieval
    - search_contracts()        # Semantic search
    - answer_question()         # Generate AI answers
    - analyze_contract()        # Contract analysis
    - assess_risk()             # Risk assessment
```

#### **early_warning.py** - Alert System
```python
class EarlyWarningSystem:
    # Warning detection
    - analyze_contract()        # Check warning criteria
    - get_all_warnings()        # Aggregate warnings
    
    # Categories:
    - Critical: Expiring ≤ 30 days
    - Warning: Expiring 31-90 days
    - Info: Expiring 91-180 days
    - Risk: High/Critical risk level
```

#### **schemas.py** - Data Models
```python
# Pydantic models for validation
- ContractCreate
- ContractUpdate
- ContractResponse
- QuestionRequest
```

#### **config.py** - Configuration
```python
# Environment-based settings
- DATABASE_URL
- GEMINI_API_KEY
- UPLOAD_DIRECTORY
- APP_NAME
```

---

## 📊 Database Design

### **Contracts Table Schema**

```sql
CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,
    contract_number VARCHAR(50) UNIQUE NOT NULL,
    contract_name VARCHAR(255) NOT NULL,
    party_a VARCHAR(255) NOT NULL,
    party_b VARCHAR(255) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    contract_value DECIMAL(15, 2),
    currency VARCHAR(10),
    risk_level VARCHAR(20) NOT NULL,
    risk_reason TEXT,
    file_path TEXT NOT NULL,
    file_type VARCHAR(10),
    summary TEXT,
    key_clauses JSON,
    compliance_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_contract_number ON contracts(contract_number);
CREATE INDEX idx_status ON contracts(status);
CREATE INDEX idx_risk_level ON contracts(risk_level);
CREATE INDEX idx_end_date ON contracts(end_date);
```

### **Database Migrations**

- **Initial Schema**: Base contract structure
- **Risk Reason**: Added detailed risk explanations
- **Indexes**: Performance optimization for queries

---

## 🔌 API Endpoints

### **Contract Management**

#### `POST /api/contracts/upload`
Upload and analyze contract files.

**Request:**
```
Content-Type: multipart/form-data
files: File[] (PDF or TXT)
```

**Response:**
```json
{
  "message": "Successfully uploaded 1 contracts",
  "contracts": [
    {
      "id": 1,
      "contract_number": "CNT-2024-0001",
      "contract_name": "Service Agreement",
      "risk_level": "medium",
      "status": "active"
    }
  ]
}
```

#### `GET /api/contracts`
List contracts with optional filters.

**Query Parameters:**
- `status`: Filter by status (active/expired/renewed/pending)
- `risk_level`: Filter by risk (low/medium/high/critical)
- `skip`: Pagination offset
- `limit`: Results per page

**Response:**
```json
[
  {
    "id": 1,
    "contract_number": "CNT-2024-0001",
    "contract_name": "Service Agreement",
    "party_a": "TechCorp",
    "party_b": "VendorMax",
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2025-01-01T00:00:00",
    "status": "active",
    "risk_level": "medium",
    "contract_value": 100000.00
  }
]
```

#### `GET /api/contracts/{id}`
Get single contract details.

#### `DELETE /api/contracts/{id}`
Delete a contract.

#### `DELETE /api/contracts/admin/clear-all?confirm=yes-delete-all`
Admin endpoint to clear all contracts.

### **Dashboard & Analytics**

#### `GET /api/dashboard/stats`
Get dashboard statistics.

**Response:**
```json
{
  "total_contracts": 120,
  "active_contracts": 45,
  "expired_contracts": 30,
  "expiring_soon": 12,
  "low_risk": 52,
  "medium_risk": 42,
  "high_risk": 19,
  "critical_risk": 7,
  "total_value": 12500000.00
}
```

#### `GET /api/warnings`
Get early warning alerts.

**Response:**
```json
{
  "critical": 5,
  "warning": 12,
  "info": 20,
  "risk": 8,
  "contracts": {
    "critical": [...],
    "warning": [...],
    "info": [...],
    "risk": [...]
  }
}
```

### **AI Features**

#### `POST /api/contracts/ask`
Ask questions using RAG.

**Request:**
```json
{
  "question": "What are the payment terms in CNT-2024-0001?",
  "contract_id": 1  // optional, for specific contract
}
```

**Response:**
```json
{
  "answer": "The payment terms are quarterly installments...",
  "contracts_searched": 15
}
```

#### `POST /api/contracts/reanalyze-all`
Bulk reanalyze all contracts.

#### `POST /api/contracts/{id}/reanalyze`
Reanalyze specific contract.

---

## 🤖 RAG Implementation

### **RAG Pipeline Architecture**

```
Document → Chunking → Embedding → Storage → Retrieval → Generation
```

### **1. Document Ingestion**

```python
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    """
    Split contract into overlapping chunks.
    
    Why overlap?
    - Maintains context across chunk boundaries
    - Prevents information loss
    - Improves retrieval accuracy
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks
```

### **2. Vector Storage**

```python
async def add_contract_to_vectordb(
    contract_id: int,
    contract_text: str,
    metadata: dict
):
    """
    Store contract chunks for semantic search.
    
    Current Implementation:
    - In-memory storage (simple, fast)
    - No external vector DB required
    
    Future Enhancement:
    - ChromaDB for persistent storage
    - Embedding caching
    - Hybrid search (keyword + semantic)
    """
    chunks = chunk_text(contract_text)
    self.contracts_storage[contract_id] = {
        "text": contract_text,
        "chunks": chunks,
        "metadata": metadata
    }
```

### **3. Semantic Search**

```python
async def search_contracts(query: str, limit: int = 5):
    """
    Find relevant contract chunks.
    
    Algorithm:
    1. Search across all contract chunks
    2. Use Gemini for semantic matching
    3. Rank by relevance
    4. Return top-k results
    """
    results = []
    for contract_id, data in self.contracts_storage.items():
        for chunk in data["chunks"]:
            # Semantic similarity check
            if is_relevant(query, chunk):
                results.append({
                    "contract_id": contract_id,
                    "chunk": chunk,
                    "metadata": data["metadata"]
                })
    return ranked_results(results, limit)
```

### **4. Answer Generation**

```python
async def answer_question(question: str, contract_id: Optional[int] = None):
    """
    Generate AI answer using retrieved context.
    
    RAG Flow:
    1. Retrieve relevant chunks
    2. Construct prompt with context
    3. Generate answer via Gemini
    4. Return structured response
    """
    # Search for relevant content
    context_chunks = await search_contracts(question, contract_id)
    
    # Build prompt with retrieved context
    prompt = f"""
    Based on these contract excerpts:
    {context_chunks}
    
    Question: {question}
    
    Provide a detailed, accurate answer.
    """
    
    # Generate response
    response = self.model.generate_content(prompt)
    return response.text
```

---

## 🧠 AI Integration

### **Google Gemini 2.5 Flash**

#### **Why Gemini?**
- ⚡ Fast inference (< 2 seconds)
- 📝 1M+ token context window
- 💰 Cost-effective ($0.075/1M tokens)
- 🎯 Strong reasoning capabilities
- 📊 JSON mode support

#### **Initialization**

```python
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')
```

#### **Key AI Tasks**

**1. Contract Analysis**
```python
async def analyze_contract(contract_text: str):
    """
    Extract metadata and generate summary.
    
    Outputs:
    - Party names
    - Contract dates
    - Contract value
    - Key terms
    - Summary
    """
```

**2. Risk Assessment**
```python
async def assess_risk(contract_text: str):
    """
    Evaluate contract risk level.
    
    Risk Factors:
    - Financial exposure
    - Compliance requirements
    - Termination clauses
    - Liability limits
    - Payment terms
    
    Returns: low/medium/high/critical + explanation
    """
```

**3. Question Answering**
```python
async def answer_question(question: str):
    """
    RAG-powered Q&A.
    
    Features:
    - Semantic search
    - Context-aware responses
    - Multi-contract queries
    - Citation support
    """
```

---

## 🚀 Deployment

### **Render Platform**

#### **Configuration (`render.yaml`)**

```yaml
services:
  - type: web
    name: contract-management-system
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: contract-management-db
          property: connectionString
      - key: GEMINI_API_KEY
        sync: false

databases:
  - name: contract-management-db
    databaseName: contract_management_db
    plan: free
    region: oregon
    version: 18
```

#### **Environment Variables**

```bash
# Production (Render)
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
GEMINI_API_KEY=your_api_key

# Local Development
DATABASE_URL=sqlite+aiosqlite:///./contracts.db
GEMINI_API_KEY=your_api_key
```

#### **Deployment Process**

1. **Push to GitHub** → `git push origin main`
2. **Auto-Deploy** → Render detects changes
3. **Build Phase** → Install dependencies
4. **Migration** → Database schema updates
5. **Start Server** → Uvicorn launches app
6. **Health Check** → Render verifies status
7. **Live** → Application accessible

### **Production URL**
```
https://contract-management-system-6v5x.onrender.com
```

---

## 🔒 Security

### **Authentication & Authorization**
- No authentication (demo/MVP phase)
- Future: JWT-based auth
- Future: Role-based access control (RBAC)

### **Data Security**
- HTTPS encryption in transit
- PostgreSQL encryption at rest
- Environment variables for secrets
- Input validation with Pydantic
- SQL injection prevention (ORM)

### **File Upload Security**
- File type validation
- Size limits
- Sanitized filenames
- Isolated storage

### **API Security**
- CORS configuration
- Rate limiting (planned)
- Request validation
- Error handling without data leaks

---

## 💻 Development Setup

### **Prerequisites**
- Python 3.14+
- PostgreSQL 16+ (for production)
- Git
- Google Gemini API key

### **Local Setup**

```bash
# 1. Clone repository
git clone https://github.com/naveenrajd123/managecontract.git
cd managecontract

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp env.example .env
# Edit .env with your GEMINI_API_KEY

# 5. Initialize database
# Database will auto-create on first run

# 6. Start server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 7. Open browser
http://localhost:8000
```

### **Project Structure**

```
managecontract/
├── src/                    # Backend source code
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   ├── database.py        # Database models & setup
│   ├── rag_system.py      # RAG implementation
│   ├── early_warning.py   # Alert system
│   ├── schemas.py         # Pydantic models
│   └── config.py          # Configuration
├── static/                 # Frontend assets
│   ├── index.html         # Main HTML
│   ├── styles.css         # Styles
│   └── app.js             # JavaScript
├── demo_contracts/         # Sample contracts
├── demo_contracts2/        # 120 test contracts
├── uploads/                # Uploaded files
├── requirements.txt        # Python dependencies
├── render.yaml            # Render config
├── runtime.txt            # Python version
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── README.md              # Project overview
├── DEPLOYMENT.md          # Deployment guide
├── TECHNICAL.md           # This file
└── BUSINESS.md            # Business documentation
```

### **Development Tools**

- **IDE**: Cursor.ai (AI-powered coding)
- **AI Assistant**: Claude Sonnet 4.5
- **Version Control**: Git + GitHub
- **Testing**: Manual testing + API testing
- **Monitoring**: Render logs + dashboard

---

## 📊 Performance Considerations

### **Optimization Strategies**

1. **Async/Await** - Non-blocking I/O operations
2. **Connection Pooling** - Database connection reuse
3. **Lazy Loading** - Load data on demand
4. **Caching** - (Future) Redis for frequently accessed data
5. **Chunking** - Process large files in chunks
6. **Pagination** - Limit API response sizes

### **Scalability**

- **Horizontal Scaling** - Multiple server instances
- **Database Scaling** - PostgreSQL read replicas
- **CDN** - Static asset delivery
- **Load Balancing** - Distribute traffic

---

## 🔮 Future Enhancements

### **Technical Roadmap**

1. **Vector Database** - ChromaDB/Pinecone for better RAG
2. **Caching Layer** - Redis for performance
3. **Background Jobs** - Celery for async tasks
4. **Webhooks** - Real-time notifications
5. **API Versioning** - Backward compatibility
6. **GraphQL** - Alternative to REST
7. **WebSockets** - Real-time updates
8. **Microservices** - Service decomposition
9. **Containerization** - Docker deployment
10. **CI/CD Pipeline** - Automated testing & deployment

---

## 📝 Development Credits

**Built with:**
- **IDE**: [Cursor.ai](https://cursor.sh) - AI-powered code editor
- **AI Assistant**: [Claude Sonnet 4.5](https://www.anthropic.com/claude) by Anthropic
- **Framework**: FastAPI + Python
- **AI Model**: Google Gemini 2.5 Flash
- **Platform**: Render

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Google Gemini API](https://ai.google.dev/)
- [Render Documentation](https://render.com/docs)
- [RAG Architecture Guide](https://www.pinecone.io/learn/retrieval-augmented-generation/)

---

**Last Updated**: January 2026  
**Version**: 1.0.0  
**Status**: Production
