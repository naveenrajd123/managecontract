"""
Pydantic Schemas
These define the data structures for API requests and responses.

Think of these as "data contracts" - they validate data going in and out.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ContractCreate(BaseModel):
    """Schema for creating a new contract."""
    contract_name: str = Field(..., description="Name of the contract")
    contract_number: str = Field(..., description="Unique contract number")
    party_a: str = Field(..., description="First party (usually your organization)")
    party_b: str = Field(..., description="Second party")
    start_date: datetime = Field(..., description="Contract start date")
    end_date: datetime = Field(..., description="Contract end date")
    status: Optional[str] = Field("active", description="Contract status")
    contract_value: Optional[float] = Field(None, description="Contract value")
    currency: Optional[str] = Field("USD", description="Currency code")
    risk_level: Optional[str] = Field("low", description="Risk level")


class ContractUpdate(BaseModel):
    """Schema for updating a contract (all fields optional)."""
    contract_name: Optional[str] = None
    party_a: Optional[str] = None
    party_b: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    contract_value: Optional[float] = None
    currency: Optional[str] = None
    risk_level: Optional[str] = None
    summary: Optional[str] = None


class ContractResponse(BaseModel):
    """Schema for contract responses."""
    id: int
    contract_name: str
    contract_number: Optional[str]  # Allow None
    party_a: Optional[str]
    party_b: Optional[str]
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
    status: str
    contract_value: Optional[float]
    currency: str
    risk_level: str
    risk_reason: Optional[str]  # AI-generated reason for risk level
    file_path: Optional[str]
    file_type: Optional[str]
    summary: Optional[str]
    key_clauses: Optional[str]
    
    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models


class QuestionRequest(BaseModel):
    """Schema for asking questions about contracts."""
    question: str = Field(..., description="The question to ask")
    contract_id: Optional[int] = Field(None, description="Optional: limit to specific contract")
