"""
Pydantic Schemas - Data Validation Models
==========================================

WHAT IS THIS FILE?
This file defines "schemas" which are like blueprints or templates that describe
what data should look like when it comes INTO our API (requests) and goes OUT of 
our API (responses).

Think of it like a form that checks:
- Is the email field actually an email?
- Is the age a number and not text?
- Are all required fields filled in?

Pydantic does this automatically for us!
"""

# ============================================================================
# IMPORTS - Bringing in tools we need from other Python libraries
# ============================================================================

from pydantic import BaseModel, Field  
# "from pydantic import" means: "From the pydantic library, bring in..."
# - BaseModel: A special class we'll use as a template for our data models
#   Think of it as a super-powered dictionary that validates data automatically
# - Field: A function that adds extra rules/descriptions to our data fields
#   Like saying "this field is required" or "this is what it means"

from datetime import datetime  
# "datetime" is Python's built-in module for working with dates and times
# We import "datetime" class from it to handle contract dates like "2024-01-15"

from typing import Optional  
# "Optional" is a type hint that means "this field can be the specified type OR None (empty)"
# Example: Optional[str] means "this can be text OR be empty"
# It's like making a field optional on a form


# ============================================================================
# CLASS 1: ContractCreate
# PURPOSE: Defines what data we need when CREATING a new contract
# ============================================================================

class ContractCreate(BaseModel):  
    # WHAT IS A CLASS?
    # A class is like a blueprint or template for creating objects
    # Like a cookie cutter - it defines the shape, and you use it to make cookies
    
    # "class ContractCreate" means: "I'm creating a new blueprint called ContractCreate"
    # "(BaseModel)" means: "This blueprint inherits/copies all features from BaseModel"
    # BaseModel gives us superpowers like automatic data validation!
    
    """Schema for creating a new contract."""  
    # This is a "docstring" - a special comment that describes what this class does
    # Triple quotes """ allow multi-line text
    
    # Below are FIELDS - these are the pieces of data our contract needs
    # Format: field_name: data_type = Field(default_value, description="what it means")
    
    contract_name: str = Field(..., description="Name of the contract")
    # contract_name: This is the field name (like a label on a form field)
    # str: This means the data type must be STRING (text), not a number or date
    # Field(...): This is a Pydantic function that adds rules
    # ...: Three dots (ellipsis) mean "THIS FIELD IS REQUIRED" - can't be empty
    # description="...": Human-readable explanation of what this field is for
    
    contract_number: str = Field(..., description="Unique contract number")
    # Same as above - a required text field for the contract's unique ID like "CNT-2024-001"
    
    party_a: str = Field(..., description="First party (usually your organization)")
    # party_a: Name of the first party in the contract (like "ABC Company")
    # Required field (because of ...)
    
    party_b: str = Field(..., description="Second party")
    # party_b: Name of the second party (like "XYZ Vendor")
    # Required field
    
    start_date: datetime = Field(..., description="Contract start date")
    # start_date: When the contract begins
    # datetime: This must be a date+time value, not just text
    # Required field
    
    end_date: datetime = Field(..., description="Contract end date")
    # end_date: When the contract expires
    # datetime: Must be a date+time value
    # Required field
    
    status: Optional[str] = Field("active", description="Contract status")
    # status: Current state of the contract (active, expired, renewed, pending)
    # Optional[str]: This field is OPTIONAL - can be text or can be empty
    # Field("active"): If not provided, default value is "active"
    # So this field is optional, but if you don't provide it, it defaults to "active"
    
    contract_value: Optional[float] = Field(None, description="Contract value")
    # contract_value: The dollar amount of the contract
    # Optional[float]: Can be a decimal number (like 25000.50) OR can be empty
    # float: Decimal number type (as opposed to int which is whole numbers)
    # Field(None): Default is None (empty) if not provided
    # None: Python's way of saying "nothing" or "empty"
    
    currency: Optional[str] = Field("USD", description="Currency code")
    # currency: What currency the contract value is in
    # Optional[str]: Can be text or empty
    # Field("USD"): Default is "USD" if not provided
    
    risk_level: Optional[str] = Field("low", description="Risk level")
    # risk_level: How risky the contract is (low, medium, high, critical)
    # Optional[str]: Can be text or empty
    # Field("low"): Default is "low" if not provided


# ============================================================================
# CLASS 2: ContractUpdate
# PURPOSE: Defines what data we need when UPDATING an existing contract
# ============================================================================

class ContractUpdate(BaseModel):  
    # Another class (blueprint) inheriting from BaseModel
    # This one is for when we want to UPDATE a contract (not create a new one)
    
    """Schema for updating a contract (all fields optional)."""  
    # Docstring: All fields here are optional because you might only want to
    # update ONE field (like just changing the status) without changing everything
    
    # Notice: ALL fields below are Optional and default to None
    # This means when updating, you only need to provide the fields you want to change
    
    contract_name: Optional[str] = None
    # Optional[str]: Can be text or None (empty)
    # = None: Default value is None (empty) if not provided
    # When updating, if you don't include this field, it won't change
    
    party_a: Optional[str] = None
    # Optional text field, defaults to None if not provided
    
    party_b: Optional[str] = None
    # Optional text field, defaults to None
    
    start_date: Optional[datetime] = None
    # Optional date field, defaults to None
    # Optional[datetime]: Can be a date OR be empty
    
    end_date: Optional[datetime] = None
    # Optional date field, defaults to None
    
    status: Optional[str] = None
    # Optional text field for status, defaults to None
    
    contract_value: Optional[float] = None
    # Optional decimal number for contract value, defaults to None
    
    currency: Optional[str] = None
    # Optional text field for currency, defaults to None
    
    risk_level: Optional[str] = None
    # Optional text field for risk level, defaults to None
    
    summary: Optional[str] = None
    # Optional text field for AI-generated summary, defaults to None


# ============================================================================
# CLASS 3: ContractResponse
# PURPOSE: Defines what data we SEND BACK when someone requests contract info
# ============================================================================

class ContractResponse(BaseModel):  
    # This class defines the structure of data we return from our API
    # When someone asks for contract details, this is what they get back
    
    """Schema for contract responses."""
    # Docstring: This is what the API sends back to the user
    
    # Notice: These fields don't use Field() - they're simpler
    # They just define what type each field should be
    
    id: int
    # id: The database ID number of this contract (like 1, 2, 3...)
    # int: Must be an INTEGER (whole number), not text or decimal
    # No Optional, no default = THIS IS REQUIRED in the response
    
    contract_name: str
    # Contract name (text), required field
    
    contract_number: Optional[str]  # Allow None
    # Contract number (text), can be empty
    # Comment explains: We allow None in case some old contracts don't have a number
    
    party_a: Optional[str]
    # First party name (text), can be empty
    
    party_b: Optional[str]
    # Second party name (text), can be empty
    
    start_date: datetime
    # Contract start date (date+time), required
    
    end_date: datetime
    # Contract end date (date+time), required
    
    created_at: datetime
    # When this contract was created in our system (date+time), required
    # Automatically set by the database when we create a new contract
    
    updated_at: datetime
    # When this contract was last updated (date+time), required
    # Automatically updated by the database every time we modify the contract
    
    status: str
    # Contract status (text), required
    # Values: "active", "expired", "renewed", or "pending"
    
    contract_value: Optional[float]
    # Contract dollar value (decimal number), can be empty
    
    currency: str
    # Currency code (text), required
    # Like "USD", "EUR", "GBP"
    
    risk_level: str
    # Risk assessment (text), required
    # Values: "low", "medium", "high", or "critical"
    
    risk_reason: Optional[str]  # AI-generated reason for risk level
    # Why the AI assigned this risk level (text), can be empty
    # This is the explanation the AI provides
    
    file_path: Optional[str]
    # Where the contract file is stored on disk (text), can be empty
    # Like: "./uploads/contract_001.pdf"
    
    file_type: Optional[str]
    # What type of file it is (text), can be empty
    # Like: ".pdf" or ".txt"
    
    summary: Optional[str]
    # AI-generated summary of the contract (text), can be empty
    
    key_clauses: Optional[str]
    # AI-extracted important clauses from the contract (text), can be empty
    # Stored as JSON string
    
    # ========================================================================
    # INNER CLASS: Config
    # This is a special class INSIDE ContractResponse that configures behavior
    # ========================================================================
    
    class Config:
        # WHAT IS AN INNER CLASS?
        # A class inside another class - used here to configure Pydantic's behavior
        # It's like settings for how ContractResponse should work
        
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models
        # from_attributes = True: This is a Pydantic setting
        # 
        # WHAT DOES IT DO?
        # It tells Pydantic: "When converting database objects to JSON responses,
        # read the data from object attributes (like contract.name) instead of 
        # requiring a dictionary"
        #
        # WHY DO WE NEED THIS?
        # Our database uses SQLAlchemy which creates objects like:
        #   contract.name = "Service Agreement"
        #   contract.value = 100000
        #
        # Without from_attributes=True, Pydantic would expect a dictionary like:
        #   {"name": "Service Agreement", "value": 100000}
        #
        # With from_attributes=True, Pydantic can work with both!


# ============================================================================
# CLASS 4: QuestionRequest
# PURPOSE: Defines data structure when user asks AI a question about contracts
# ============================================================================

class QuestionRequest(BaseModel):  
    # This class defines what data is needed when someone asks the AI a question
    # Like when you use the "Ask AI" feature in the app
    
    """Schema for asking questions about contracts."""
    # Docstring: Used for the RAG (Retrieval Augmented Generation) Q&A feature
    
    question: str = Field(..., description="The question to ask")
    # question: The actual question text from the user
    # str: Must be text (not a number)
    # Field(...): Required field (can't be empty)
    # description: Explains what this field is for
    # 
    # Example: "What are the payment terms in contract CNT-2024-001?"
    
    contract_id: Optional[int] = Field(None, description="Optional: limit to specific contract")
    # contract_id: If provided, only search this specific contract
    # Optional[int]: Can be a whole number OR be empty
    # Field(None): Default is None (empty) - means "search all contracts"
    # 
    # HOW IT WORKS:
    # - If contract_id is None: AI searches ALL contracts
    # - If contract_id is 5: AI only searches contract with ID 5
    #
    # Example usage:
    # {"question": "What's the termination clause?", "contract_id": 5}
    # vs
    # {"question": "Show me all payment terms", "contract_id": None}


# ============================================================================
# KEY CONCEPTS SUMMARY
# ============================================================================
"""
1. IMPORTS:
   - Bring in code from other files/libraries to use here

2. CLASSES:
   - Blueprints/templates for creating objects
   - Like a form that defines what fields are needed

3. BaseModel (from Pydantic):
   - A special class that automatically validates data
   - Checks if data types are correct (text vs number)
   - Checks if required fields are provided
   - Converts data between formats (JSON ↔ Python objects)

4. TYPE HINTS (str, int, float, datetime):
   - Tell Python what type of data a variable should be
   - str = text, int = whole number, float = decimal, datetime = date+time

5. Optional[type]:
   - Means field can be the specified type OR None (empty)
   - Optional[str] = can be text or empty

6. Field():
   - Adds extra rules and descriptions to fields
   - ... = required, can't be empty
   - "text" = default value if not provided
   - None = default is empty if not provided

7. None:
   - Python's way of saying "nothing" or "empty"
   - Like a blank field on a form

8. INHERITANCE (class MyClass(BaseModel)):
   - MyClass "inherits" all features from BaseModel
   - Like getting all your parent's traits
   - We get validation superpowers from BaseModel!

9. DOCSTRINGS (triple quotes """):
   - Special comments that describe what code does
   - Useful for documentation

10. WHY WE NEED SCHEMAS:
    - Validate incoming data (is it the right format?)
    - Define what data to return in API responses
    - Auto-generate API documentation
    - Prevent bugs from bad data
    - Make code self-documenting

REAL-WORLD ANALOGY:
Imagine you're at a restaurant:
- ContractCreate = The order form you fill out (what you send to kitchen)
- ContractUpdate = Modifying your order (change side dish)
- ContractResponse = The meal you get back (what kitchen sends you)
- QuestionRequest = Asking the waiter a question

The schemas make sure:
- Your order form is filled out correctly
- The kitchen sends you what you ordered
- Everyone understands what's being requested/delivered
"""