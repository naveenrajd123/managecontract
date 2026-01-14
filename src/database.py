"""
Database Setup and Models
This file defines:
1. How we connect to the database
2. What data structure we use for contracts
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.config import settings

# Base class for all database models
Base = declarative_base()


class Contract(Base):
    """
    Contract Model - Defines what information we store for each contract.
    
    Think of this like a spreadsheet where each contract is a row,
    and these are the columns.
    """
    __tablename__ = "contracts"
    
    # Primary key - unique ID for each contract
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic contract information
    contract_name = Column(String(255), nullable=False, index=True)
    contract_number = Column(String(100), unique=True, index=True)
    
    # Parties involved
    party_a = Column(String(255))  # Our organization
    party_b = Column(String(255))  # Other party
    
    # Important dates
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Contract status
    status = Column(String(50), default="active")  # active, expired, renewed, pending
    
    # Financial information
    contract_value = Column(Float, nullable=True)
    currency = Column(String(10), default="USD")
    
    # Risk classification
    risk_level = Column(String(20), default="low")  # low, medium, high, critical
    risk_reason = Column(Text, nullable=True)  # AI-generated reason for risk level
    
    # File information
    file_path = Column(String(500))  # Where the actual contract file is stored
    file_type = Column(String(50))   # pdf, docx, etc.
    
    # AI-generated summary
    summary = Column(Text, nullable=True)
    
    # Key clauses extracted by AI
    key_clauses = Column(Text, nullable=True)  # Stored as JSON string
    
    # Compliance and legal
    compliance_notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Contract(id={self.id}, name={self.contract_name}, status={self.status})>"


# Database engine and session setup
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Session maker for database operations
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """
    Initialize the database - create all tables.
    Call this when the application starts.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """
    Dependency function to get database session.
    This is used by FastAPI to inject database access into API endpoints.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
