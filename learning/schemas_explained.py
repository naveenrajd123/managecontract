"""
schemas.py - FULLY EXPLAINED FOR BEGINNERS
==========================================

This is a detailed, line-by-line explanation of schemas.py to help you learn Python!
"""

# =============================================================================
# LINE-BY-LINE EXPLANATION
# =============================================================================

# LINE 8: from pydantic import BaseModel, Field
# -----------------------------------------------
# WHAT IT MEANS:
# "from X import Y" = Get specific tools from a library
# "pydantic" = A Python library for data validation
# "BaseModel" = A special class that validates data automatically
# "Field" = A function to add rules to our fields

# ANALOGY: It's like saying "From my toolbox, get me the hammer and screwdriver"

# BaseModel gives us:
# - Automatic type checking (is this text? a number?)
# - Required field validation (did they fill it in?)  
# - JSON conversion (turn Python objects into web-friendly format)

# Field() lets us add:
# - Descriptions (what is this field for?)
# - Default values (what if they don't provide it?)
# - Validation rules (must be positive number, etc.)


# LINE 9: from datetime import datetime
# --------------------------------------
# WHAT IT MEANS:
# Get the "datetime" class from Python's built-in "datetime" module
# This is for working with dates and times

# EXAMPLES:
# datetime.now() = Current date/time
# datetime(2024, 1, 15) = January 15, 2024


# LINE 10: from typing import Optional
# -------------------------------------
# WHAT IT MEANS:
# Get "Optional" from Python's typing system
# Optional[X] = This can be type X OR it can be None (empty)

# EXAMPLES:
# age: int = 25  # Must be a number
# age: Optional[int] = None  # Can be a number OR empty

# REAL WORLD: Like a form where some fields are optional


# LINE 13: class ContractCreate(BaseModel):
# ------------------------------------------
# WHAT IS A CLASS?
# A class is a blueprint/template for creating objects
# Like a cookie cutter - defines the shape

# BREAKDOWN:
# "class" = Python keyword to create a new class
# "ContractCreate" = Name we chose for this class
# "(BaseModel)" = Inherit from BaseModel (get its superpowers)

# WHAT IS INHERITANCE?
# Like a child getting traits from parents
# ContractCreate gets all of BaseModel's validation abilities

# WHY?
# Instead of writing validation code ourselves, we inherit it from BaseModel!


# LINE 15: contract_name: str = Field(..., description="Name of the contract")
# -----------------------------------------------------------------------------
# THIS IS A FIELD DEFINITION - Let's break it down piece by piece:

# "contract_name" = The name of this field (like a label on a form)

# ": str" = Type hint - this must be a STRING (text)
#   str = string (text like "Service Agreement")
#   int = integer (whole number like 5)
#   float = decimal (like 25.50)
#   datetime = date and time
#   bool = True or False

# "=" = Assignment - we're setting a value

# "Field()" = A Pydantic function that adds rules

# "..." = Ellipsis (three dots) means REQUIRED
#   If someone tries to create a contract without a name, Pydantic will reject it!

# "description=" = Human-readable explanation
#   Helps developers and auto-generates API documentation


# LINE 21: status: Optional[str] = Field("active", description="Contract status")
# -------------------------------------------------------------------------------
# Let's break this down:

# "status" = Field name

# ": Optional[str]" = Type hint with Optional
#   Optional[str] = Can be a STRING or can be None (empty)
#   Without Optional: Must provide a value
#   With Optional: Can leave it empty

# "= Field("active", ...)" = Set default value
#   If you don't provide a status, it defaults to "active"
#   So this field is technically optional because it has a default


# LINE 22: contract_value: Optional[float] = Field(None, description="Contract value")
# ------------------------------------------------------------------------------------
# "contract_value" = Field name

# ": Optional[float]" = Can be a decimal number OR empty
#   float = Floating point number (decimal) like 25000.50
#   Not int (whole number) because contracts can have cents

# "= Field(None, ...)" = Default value is None
#   None = Python's special value meaning "nothing" or "empty"
#   Like leaving a form field blank


# LINE 27-38: class ContractUpdate(BaseModel):
# ---------------------------------------------
# Another class for UPDATING contracts
# Key difference from ContractCreate:
# - ALL fields are Optional
# - ALL default to None
# - You only send the fields you want to change

# Example: To only change status:
# {"status": "expired"}
# You don't need to send all the other fields!


# LINE 41-60: class ContractResponse(BaseModel):
# -----------------------------------------------
# This defines what data we SEND BACK to users
# Notice: Some fields are required (no Optional)
# Some are Optional (can be empty)

# Example Response:
# {
#   "id": 1,
#   "contract_name": "Service Agreement",
#   "status": "active",
#   "risk_level": "medium"
# }


# LINE 43: id: int
# ----------------
# Simple field definition:
# "id" = Field name
# ": int" = Must be an integer (whole number)
# No "= Field()" needed for simple types
# No Optional = This is REQUIRED


# LINE 62-63: class Config:
# --------------------------
# WHAT IS THIS?
# A special inner class that configures Pydantic's behavior
# It's like settings for the ContractResponse class

# "class Config:" = Start of configuration class
# This is a nested class (class inside a class)


# LINE 63: from_attributes = True
# --------------------------------
# WHAT DOES THIS DO?
# Tells Pydantic: "Read data from object attributes, not just dictionaries"

# WITHOUT from_attributes=True:
# response = {"name": "Contract", "value": 100}  # Must be dictionary
# ContractResponse(**response)  # Works

# WITH from_attributes=True:
# contract = database_object  # SQLAlchemy object
# contract.name = "Contract"
# contract.value = 100
# ContractResponse.from_orm(contract)  # Works! Can read from object


# LINE 66-69: class QuestionRequest(BaseModel):
# ----------------------------------------------
# Schema for the AI Q&A feature

# When user asks: "What are the payment terms?"
# We send: {"question": "What are the payment terms?", "contract_id": null}

# If asking about specific contract:
# {"question": "What is the termination clause?", "contract_id": 5}


# =============================================================================
# KEY PYTHON CONCEPTS EXPLAINED
# =============================================================================

"""
1. TYPE HINTS (the : str, : int, : datetime stuff)
   Purpose: Tell Python what type of data to expect
   Benefits:
   - Catches errors early (you put text where number expected)
   - Makes code self-documenting
   - IDEs can give better suggestions

2. Optional[type]
   Optional[str] = Can be string OR None
   Used for fields that aren't required

3. None
   Python's "nothing" value
   Like an empty box or blank form field
   
4. Field()
   Pydantic function to add validation rules
   - Field(...) = Required
   - Field("default") = Optional with default value
   - Field(None) = Optional, defaults to empty

5. BaseModel
   Pydantic's superclass that gives us:
   - Automatic validation
   - JSON conversion
   - API documentation
   - Error messages

6. class MyClass(ParentClass)
   Creates a new class that inherits from ParentClass
   Gets all of ParentClass's methods and features

7. Docstrings (triple quotes)
   Special comments that describe code
   Used for documentation generation

8. from X import Y
   Get specific items from a module/library
   Like taking specific tools from a toolbox
"""


# =============================================================================
# REAL-WORLD ANALOGY
# =============================================================================

"""
Think of schemas like forms at a doctor's office:

ContractCreate = New Patient Form
- Name: _________ (required)
- DOB: _________ (required)
- Phone: _________ (optional, but defaults to "No phone")

ContractUpdate = Update Info Form
- Name: _________ (optional - only if changing)
- Address: _________ (optional - only if changing)
You only fill out what you're changing!

ContractResponse = Your Medical Record Print-Out
- Patient ID: 12345 (always included)
- Name: John Doe (always included)
- Notes: "..." (might be empty if no notes)

The schemas ensure:
✓ Required fields are filled
✓ Data is the right type (text vs number)
✓ Optional fields have defaults
✓ Everyone knows what to expect
"""


# =============================================================================
# WHY WE NEED SCHEMAS
# =============================================================================

"""
1. DATA VALIDATION
   Automatically checks if data is correct
   Example: Rejects if someone sends "abc" for a number field

2. AUTO-DOCUMENTATION
   FastAPI uses schemas to generate interactive API docs
   Developers can see what fields are needed

3. TYPE SAFETY
   Catches errors before they cause problems
   IDE warns you: "This expects a number, you're sending text"

4. CONSISTENCY
   Everyone uses the same data structure
   Frontend, backend, database all agree on format

5. MAINTENANCE
   When you need to add a field, change it in one place
   All code using the schema updates automatically

6. ERROR MESSAGES
   Pydantic gives helpful errors:
   "Field 'contract_name' is required"
   "Field 'contract_value' must be a number"
"""
