# 📄 Contract Management System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered Contract Management System with Early Warning capabilities, built with Google Gemini AI and RAG (Retrieval Augmented Generation).

> 🎯 **Perfect for**: Legal teams, procurement departments, and businesses managing multiple contracts

### ✨ Key Highlights

- 🤖 **AI-Powered Analysis** - Automatic contract summarization and risk assessment
- 📊 **Smart Dashboard** - Real-time contract monitoring and analytics
- ⚠️ **Early Warnings** - Proactive alerts for expirations and renewals
- 💬 **Natural Language Q&A** - Ask questions about your contracts in plain English
- 🔍 **Semantic Search** - Find relevant contract clauses instantly
- 📈 **Risk Management** - Automated risk level classification

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/naveenrajd123/ManageContract.git
cd ManageContract

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp env.example .env
# Edit .env and add your actual API key

# Run the application
python main.py
```

Visit http://localhost:8000 to see your dashboard! 🎉

## 🌟 Features

- **AI-Powered Analysis**: Automatically summarize contracts, extract key clauses, and assess risk levels
- **RAG System**: Ask questions about your contracts in natural language
- **Early Warning System**: Get alerts for contract expirations, renewals, and high-risk contracts
- **Smart Search**: Semantic search across all contracts using vector embeddings
- **Beautiful Dashboard**: Modern, responsive web interface
- **File Upload**: Support for PDF and TXT contract files
- **Risk Assessment**: Automatic risk level classification (Low, Medium, High, Critical)

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI
- **AI**: Google Gemini API
- **Vector Database**: ChromaDB (for RAG)
- **Database**: SQLite (via SQLAlchemy)
- **Frontend**: HTML, CSS, JavaScript
- **Document Processing**: PyPDF2

## 📋 Prerequisites

Before you begin, make sure you have:

1. **Python 3.8 or higher** installed
   - Check: `python --version` or `python3 --version`
   - Download from: https://www.python.org/downloads/

2. **Google Gemini API Key**
   - Get it free from: https://makersuite.google.com/app/apikey
   - You'll need a Google account

## 🏗️ Project Organization

The project follows a clean, modular structure:

- **`src/`** - Core application code (all Python modules)
- **`scripts/`** - Utility scripts for maintenance and testing
- **`static/`** - Frontend assets (HTML, CSS, JavaScript)
- **`data/`** - Sample contract data for testing
- **`uploads/`** - User-uploaded contracts (gitignored)

This structure makes it easy to:
- Navigate and maintain the codebase
- Import modules consistently
- Deploy to production
- Run tests and scripts

## 🚀 Setup Instructions

### Step 1: Create a Virtual Environment (Recommended)

A virtual environment keeps your project dependencies isolated.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### Step 2: Install Dependencies

This installs all required Python packages:

```bash
pip install -r requirements.txt
```

This may take a few minutes. You'll see packages being downloaded and installed.

### Step 3: Configure Environment Variables

1. Create a file named `.env` in the project root directory
2. Add your Google Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./contracts.db
APP_NAME=Contract Management System
DEBUG=True
```

**Important:** Replace `your_actual_api_key_here` with your real API key from Google!

### Step 4: Run the Application

Start the server:

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload
```

You should see:
```
✅ Contract Management System started successfully!
📊 Database: sqlite+aiosqlite:///./contracts.db
🤖 AI Model: Google Gemini
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 5: Access the Application

Open your web browser and go to:

**🌐 http://localhost:8000**

You should see the beautiful dashboard!

## 📖 How to Use

### 1. Upload a Contract

1. Click on the **"⬆️ Upload Contract"** tab
2. Fill in the contract details:
   - Contract Name (e.g., "Software License Agreement")
   - Contract Number (e.g., "CNT-2024-001")
   - Party A (Your organization)
   - Party B (Other party)
   - Start Date and End Date
   - Optional: Contract Value and Currency
3. Select a PDF or TXT file
4. Click **"📤 Upload & Analyze"**

The AI will automatically:
- Generate a summary
- Extract key clauses
- Assess risk level
- Store in the vector database for RAG

### 2. View Contracts

- Click on **"📋 All Contracts"** tab
- See all your contracts with details
- Filter by status (Active, Expired, etc.)
- View AI-generated summaries

### 3. Monitor Warnings

The dashboard shows active warnings for:
- **Critical** (Red): Contracts expiring in 30 days or less
- **Warning** (Yellow): Contracts expiring in 90 days or less
- **Info** (Blue): Contracts expiring in 180 days or less
- **High Risk**: Contracts marked as high or critical risk

### 4. Ask AI Questions (RAG)

1. Click on **"🤖 Ask AI"** tab
2. Optionally select a specific contract (or search all contracts)
3. Type your question:
   - "What are the payment terms?"
   - "Which contracts have termination clauses?"
   - "Summarize the renewal terms"
4. Click **"💬 Ask AI"**

The system uses RAG to:
1. Find relevant contract sections
2. Send them to Gemini AI
3. Generate accurate answers based on actual contract content

## 🔧 API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all API endpoints directly from the browser!

## 📁 Project Structure

```
ManageContract/
├── main.py              # Main entry point (imports from src/)
├── src/                 # Core application code
│   ├── __init__.py      # Package initialization
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database models and setup
│   ├── rag_system.py    # RAG implementation with Gemini
│   ├── early_warning.py # Warning system logic
│   ├── config.py        # Configuration management
│   └── schemas.py       # Pydantic schemas for API
├── scripts/             # Utility scripts
│   ├── generate_sample_contracts.py    # Generate test contracts
│   ├── clear_db_auto.py                # Clear database
│   ├── backfill_risk_reasons.py        # Backfill risk analysis
│   ├── migrate_add_risk_reason.py      # Database migration
│   └── generate_advanced_contracts.py  # Advanced contract generator
├── static/              # Frontend files
│   ├── index.html       # Main HTML page
│   ├── styles.css       # Styling
│   └── app.js           # JavaScript functionality
├── data/                # Sample contract data
│   ├── contracts/       # Basic sample contracts
│   ├── contracts_advanced/  # Advanced samples
│   └── contracts_diverse/   # Diverse samples
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version for deployment
├── .env                 # Environment variables (create this!)
├── .gitignore          # Git ignore file
├── README.md           # This file
├── DEPLOYMENT.md       # Deployment guide
├── PROJECT_CONTEXT.md  # Project documentation
├── render.yaml         # Render deployment config
├── start.bat           # Windows startup script
├── uploads/            # Uploaded contract files (auto-created)
└── contracts.db        # SQLite database (auto-created)
```

## 🧠 Understanding RAG (For Beginners)

**RAG = Retrieval Augmented Generation**

Think of it like an open-book exam:

1. **Retrieval**: Find relevant information in the books (contracts)
2. **Augmented**: Give that information to the AI
3. **Generation**: AI generates answer based on actual content

**Without RAG**: AI might hallucinate or make up information

**With RAG**: AI answers based on your actual contracts!

### How It Works:

1. **Document Chunking**: Split long contracts into smaller pieces
2. **Embeddings**: Convert text to mathematical vectors (numbers)
3. **Vector Database**: Store embeddings in ChromaDB
4. **Semantic Search**: Find relevant chunks by meaning, not just keywords
5. **Context Injection**: Send relevant chunks to Gemini
6. **Answer Generation**: Gemini generates answer using actual contract content

## 🎯 Key Concepts Explained

### Vector Database (ChromaDB)
- Stores text as mathematical vectors
- Enables "semantic search" - finding by meaning
- Example: "payment terms" matches "compensation agreement"

### Embeddings
- Converting text to numbers that capture meaning
- Similar concepts have similar numbers
- Allows AI to understand context

### Early Warning System
- Monitors contract dates automatically
- Calculates days until expiration
- Classifies by urgency (Critical, Warning, Info)

## 🔒 Security Notes

- Keep your `.env` file private (never commit to Git)
- The `.gitignore` file prevents accidental commits
- API key should never be shared publicly
- For production, use proper authentication

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "API key not configured"
- Check your `.env` file exists
- Verify `GEMINI_API_KEY` is set correctly
- Make sure no spaces around the = sign

### "Port already in use"
```bash
# Use a different port
uvicorn main:app --port 8080
```

### Database errors
```bash
# Delete and recreate database
rm contracts.db
python main.py
```

### PDF not processing
- Make sure the PDF isn't encrypted
- Try converting to TXT first
- Check file size (< 10MB recommended)

## 📚 Learning Resources

### Python & FastAPI
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### AI & RAG
- [Google Gemini Docs](https://ai.google.dev/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [What is RAG?](https://www.promptingguide.ai/research/rag)

### Web Development
- [HTML & CSS Tutorial](https://www.w3schools.com/)
- [JavaScript Guide](https://javascript.info/)

## 🤝 Need Help?

If you're stuck:

1. Check the error message carefully
2. Read the relevant section in this README
3. Check the API documentation at `/docs`
4. Look at the console logs (both terminal and browser)
5. Make sure all dependencies are installed

## 🛠️ Utility Scripts

The `scripts/` folder contains helpful utilities:

### Generate Sample Contracts
```bash
python scripts/generate_sample_contracts.py
```
Creates realistic sample contracts for testing.

### Clear Database
```bash
python scripts/clear_db_auto.py
```
Removes all contracts from the database (use with caution!).

### Backfill Risk Reasons
```bash
python scripts/backfill_risk_reasons.py
```
Re-analyzes contracts to add AI-generated risk reasons.

### Database Migration
```bash
python scripts/migrate_add_risk_reason.py
```
Adds the risk_reason column to existing databases.

## 🎓 Next Steps

Want to enhance the system? Try:

1. **Add more file types**: Support DOCX, DOC
2. **Email notifications**: Send alerts via email
3. **User authentication**: Add login system
4. **Advanced search**: Filter by date ranges, values
5. **Export reports**: Generate PDF reports
6. **Calendar integration**: Sync with Google Calendar
7. **Approval workflows**: Add contract approval process

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows the project structure and includes appropriate documentation.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Google Gemini AI](https://ai.google.dev/)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- Database by [SQLAlchemy](https://www.sqlalchemy.org/)

## 📧 Contact

**Naveen Raj** - [@naveenrajd123](https://github.com/naveenrajd123)

Project Link: [https://github.com/naveenrajd123/ManageContract](https://github.com/naveenrajd123/ManageContract)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Happy Contract Managing! 🎉**

Built with ❤️ for better contract management
