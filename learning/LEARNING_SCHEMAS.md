# 📚 Understanding schemas.py - Complete Beginner's Guide

## 🎯 What You'll Learn

This guide explains `schemas.py` line-by-line for Python beginners. By the end, you'll understand:
- What Pydantic is and why we use it
- How classes work
- What type hints mean
- How data validation works

---

## 📖 Quick Reference

### Common Terms You'll See

| Term | Meaning | Example |
|------|---------|---------|
| `from X import Y` | Get tool Y from library X | `from pydantic import BaseModel` |
| `class MyClass` | Create a blueprint/template | `class ContractCreate` |
| `(BaseModel)` | Inherit from BaseModel | Get validation superpowers |
| `: str` | Type hint - must be text | `name: str` |
| `: int` | Type hint - must be whole number | `age: int` |
| `: float` | Type hint - must be decimal | `price: float` |
| `: datetime` | Type hint - must be date+time | `start_date: datetime` |
| `Optional[X]` | Can be type X or None (empty) | `Optional[str]` |
| `None` | Python's "nothing" value | Like a blank field |
| `Field(...)` | Required field | Must provide value |
| `Field("default")` | Optional with default | Uses "default" if not provided |
| `Field(None)` | Optional, empty default | Empty if not provided |

---

## 🔍 Line-by-Line Breakdown

### Part 1: Imports (Getting Our Tools)

```python
from pydantic import BaseModel, Field
```

**What it means:**
- "From the pydantic library, bring in BaseModel and Field"

**What is Pydantic?**
- A library that validates data automatically
- Like a security guard checking if data is correct before letting it in

**What is BaseModel?**
- A special class we use as a template
- Gives us automatic validation superpowers

**What is Field?**
- A function to add rules and descriptions to our data fields
- Like adding labels and requirements to form fields

**Analogy:**
```
Imagine a form at the DMV:
- BaseModel = The form template
- Field() = The rules on each line ("Required", "Must be 18+", etc.)
```

---

```python
from datetime import datetime
```

**What it means:**
- Get Python's datetime tool for working with dates and times

**Examples:**
```python
datetime.now()           # Current date/time
datetime(2024, 1, 15)    # January 15, 2024
```

---

```python
from typing import Optional
```

**What it means:**
- Get the Optional tool for marking fields as "not required"

**How it works:**
```python
name: str              # Must provide a name (required)
nickname: Optional[str]  # Can provide nickname OR leave empty
```

**Analogy:**
```
Restaurant order form:
- Main dish: ________ (required)
- Side dish: ________ (optional)
```

---

### Part 2: Creating a Contract (ContractCreate)

```python
class ContractCreate(BaseModel):
```

**Let's break this down:**

**What is `class`?**
- Python keyword to create a blueprint/template
- Like a cookie cutter - defines the shape

**What is `ContractCreate`?**
- The name we chose for this blueprint
- Could be anything, but this name describes its purpose

**What is `(BaseModel)`?**
- Means: "Inherit from BaseModel"
- Like a child getting traits from parents
- We get all of BaseModel's validation abilities!

**Real-world analogy:**
```
class Car(Vehicle):
    # Car is a type of Vehicle
    # Car inherits wheels, engine, etc. from Vehicle
    # But adds car-specific features
```

---

```python
contract_name: str = Field(..., description="Name of the contract")
```

**This is a field definition - let's examine each piece:**

| Part | What It Means | Example |
|------|---------------|---------|
| `contract_name` | Field name (label) | Like "Name" on a form |
| `: str` | Type hint - must be text | `"Service Agreement"` |
| `= Field()` | Adding validation rules | Sets requirements |
| `...` | Three dots = REQUIRED | Must provide value |
| `description=` | Human explanation | What this field is for |

**Complete breakdown:**
```python
contract_name           # Name of this field
:                       # "is of type"
str                     # String (text)
=                       # "is set to"
Field(                  # Pydantic validation function
    ...                 # Ellipsis = Required!
    description="..."   # Explanation
)
```

**What does `...` (ellipsis) mean?**
- Three dots mean: **"THIS IS REQUIRED"**
- If someone tries to create a contract without a name, Pydantic rejects it
- It's like a red asterisk (*) on required form fields

---

```python
status: Optional[str] = Field("active", description="Contract status")
```

**Breaking down Optional fields:**

| Component | Meaning |
|-----------|---------|
| `Optional[str]` | Can be text OR empty |
| `Field("active", ...)` | Default value is "active" |

**How it works:**
```python
# If you provide a status:
{"status": "expired"}  # Uses "expired"

# If you don't provide a status:
{}  # Automatically uses "active"
```

**Why Optional?**
- Makes the field not required
- But still has a sensible default
- Like a checkbox that's already checked but you can uncheck it

---

```python
contract_value: Optional[float] = Field(None, description="Contract value")
```

**Understanding float and None:**

**What is `float`?**
- Decimal number (has a decimal point)
- Examples: `25000.50`, `100.00`, `3.14`
- Different from `int` (whole numbers): `25`, `100`, `3`

**Why use float for money?**
- Money has cents: $25,000.50
- `int` would only allow: $25,000 (no cents)

**What is `None`?**
- Python's special value for "nothing" or "empty"
- Not zero (0) - zero is a number
- Not empty string ("") - that's text
- Literally "nothing"

**Examples:**
```python
price = 100       # Has a value
price = None      # Empty/no value
price = 0         # Has a value (zero)
```

**Field(None) means:**
- This field is optional
- If not provided, it's empty (None)
- User can add value later

---

### Part 3: Updating a Contract (ContractUpdate)

```python
class ContractUpdate(BaseModel):
    contract_name: Optional[str] = None
    party_a: Optional[str] = None
    # ... all fields are Optional with default None
```

**Why are ALL fields Optional here?**

**The difference between Create and Update:**

| Operation | Required Fields | Why? |
|-----------|----------------|------|
| **Create** | Many required | Creating new = need basic info |
| **Update** | All optional | Changing existing = only send what changes |

**Real-world example:**
```python
# Creating a new contract - need basic info:
ContractCreate({
    "contract_name": "Service Agreement",  # Required
    "contract_number": "CNT-001",          # Required
    "party_a": "ABC Corp",                 # Required
    "party_b": "XYZ Vendor",               # Required
    # ... other required fields
})

# Updating existing contract - only send changes:
ContractUpdate({
    "status": "expired"  # Only changing status
})
# Don't need to re-send name, parties, dates, etc.!
```

**Analogy:**
```
New bank account form (ContractCreate):
- Name: ________ (required)
- Address: ________ (required)
- SSN: ________ (required)

Update address form (ContractUpdate):
- New Address: ________ (only this)
Don't need to re-enter name and SSN!
```

---

### Part 4: Responding with Contract Data (ContractResponse)

```python
class ContractResponse(BaseModel):
    id: int
    contract_name: str
    contract_number: Optional[str]
    # ...
```

**What's different here?**

| Field Type | Meaning | Why? |
|------------|---------|------|
| `id: int` | Simple type, no Field() | Cleaner for responses |
| No `= Field(...)` | No defaults needed | Database provides values |
| Mix of required and Optional | Some always exist, some might not | Realistic data |

**Understanding the fields:**

```python
id: int  
# Always has value (database auto-generates)
# Never Optional because every row has an ID

contract_name: str
# Always has value (required when creating)
# Never Optional for same reason

contract_number: Optional[str]
# Might be empty for old contracts
# Optional because legacy data might not have it

risk_reason: Optional[str]
# Might be empty if AI hasn't analyzed yet
# Optional because it's generated later
```

---

```python
class Config:
    from_attributes = True
```

**What is this inner class?**

**Class inside a class:**
- `Config` is a class nested inside `ContractResponse`
- Used to configure Pydantic's behavior
- Like settings for how the parent class works

**What does `from_attributes = True` do?**

**Without it:**
```python
# Pydantic expects dictionary:
data = {"name": "Contract", "value": 100}
ContractResponse(**data)  # Works
```

**With it:**
```python
# Pydantic can also read object attributes:
contract = database.get_contract(1)  # SQLAlchemy object
contract.name    # "Contract"
contract.value   # 100
ContractResponse.from_orm(contract)  # Works!
```

**Why we need it:**
- Our database (SQLAlchemy) creates objects, not dictionaries
- `from_attributes=True` lets Pydantic work with these objects
- Without it, we'd have to manually convert to dictionaries

**Analogy:**
```
from_attributes = True is like a universal translator:

Database speaks: object.name, object.value
Pydantic speaks: dict["name"], dict["value"]

The translator lets them understand each other!
```

---

### Part 5: Asking Questions (QuestionRequest)

```python
class QuestionRequest(BaseModel):
    question: str = Field(..., description="The question to ask")
    contract_id: Optional[int] = Field(None, description="Optional: limit to specific contract")
```

**How this works:**

**Scenario 1: Ask about all contracts**
```python
{
    "question": "Show me all payment terms",
    "contract_id": None  # or omit this field
}
# AI searches ALL contracts
```

**Scenario 2: Ask about specific contract**
```python
{
    "question": "What is the termination clause?",
    "contract_id": 5  # Only search contract #5
}
```

**Why `Optional[int]` for contract_id?**
- Sometimes want to search all contracts (None)
- Sometimes want specific contract (5)
- Flexibility!

---

## 🎓 Key Concepts Explained

### 1. Type Hints

**What are they?**
```python
name: str       # This variable should be text
age: int        # This variable should be a whole number
price: float    # This variable should be a decimal
```

**Why use them?**
- Makes code self-documenting
- Catches errors early
- IDEs give better suggestions
- Pydantic uses them for validation

**Common types:**
```python
str        # Text: "hello", "contract-001"
int        # Whole number: 1, 42, -5
float      # Decimal: 3.14, 25.50, -0.5
bool       # True or False
datetime   # Date and time
list       # [1, 2, 3]
dict       # {"key": "value"}
```

### 2. Optional

**What does it mean?**
```python
Optional[str]  # Can be string OR None
Optional[int]  # Can be integer OR None
```

**When to use:**
```python
# Required field:
name: str  # Must provide

# Optional field:
middle_name: Optional[str]  # Can omit
```

### 3. None vs Zero vs Empty String

```python
None    # Nothing, empty, no value
0       # The number zero (has a value!)
""      # Empty text (has a value - empty text!)

# Examples:
age = None  # Age not provided
age = 0     # Age is zero (newborn)
name = None  # Name not provided
name = ""    # Name is empty string
```

### 4. Field() Function

**Syntax:**
```python
Field(default_value, description="explanation")
```

**Options:**
```python
Field(...)               # Required, no default
Field("active")          # Optional, default "active"
Field(None)              # Optional, default None
Field(ge=0)              # Greater than or equal to 0
Field(max_length=100)    # Max 100 characters
```

### 5. Class Inheritance

**Basic concept:**
```python
class Animal:
    def breathe(self):
        return "breathing"

class Dog(Animal):
    # Dog inherits breathe() from Animal
    def bark(self):
        return "woof"

dog = Dog()
dog.breathe()  # Works! Inherited from Animal
dog.bark()     # Works! Defined in Dog
```

**In our code:**
```python
class ContractCreate(BaseModel):
    # Inherits validation from BaseModel
    # Gets automatic type checking
    # Gets JSON conversion
    # Gets error handling
```

---

## 🌟 Real-World Analogies

### Schemas = Forms

```
ContractCreate = "New Customer Form"
┌─────────────────────────────┐
│ Name: _________ (required)  │
│ Email: _________ (required) │
│ Phone: _________ (optional) │
└─────────────────────────────┘

ContractUpdate = "Update Info Form"
┌──────────────────────────────┐
│ Change what? ________        │
│ New value: ________          │
└──────────────────────────────┘

ContractResponse = "Receipt/Confirmation"
┌─────────────────────────────┐
│ ✓ Customer ID: 12345        │
│ ✓ Name: John Doe            │
│ ✓ Status: Active            │
└─────────────────────────────┘
```

### Type Hints = Labels

```
Without type hints:
box = something  # What's in the box? ¯\_(ツ)_/¯

With type hints:
age: int = 25    # Clearly a number!
name: str = "Bob"  # Clearly text!
```

### Pydantic = Security Guard

```
Data coming in → Pydantic checks it → Database
                    ↓
                If wrong:
                - Wrong type? REJECTED!
                - Missing required? REJECTED!
                - Invalid format? REJECTED!
```

---

## 💡 Common Questions

**Q: Why not just use dictionaries?**
```python
# Without Pydantic:
contract = {"name": "Contract", "value": "not a number!"}
# Bug! Value should be number, but no check

# With Pydantic:
contract = ContractCreate(name="Contract", value="not a number!")
# Error! Pydantic catches it immediately
```

**Q: What if I don't provide an Optional field?**
```python
# Field with default:
status: Optional[str] = Field("active")
# Result: Uses "active"

# Field with None:
notes: Optional[str] = Field(None)
# Result: Stays None (empty)
```

**Q: Can I use my own types?**
```python
# Yes! You can create custom types:
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"

# Then use it:
status: Status
```

---

## 📝 Practice Exercises

**Exercise 1: Identify field properties**
```python
price: Optional[float] = Field(0.0, description="Item price")

Questions:
1. Is this field required or optional?
2. What happens if you don't provide a value?
3. What type of data does it accept?

Answers:
1. Optional (has Optional)
2. Defaults to 0.0
3. Decimal numbers (float)
```

**Exercise 2: Fix the errors**
```python
# This has problems - can you fix them?
class Product(BaseModel):
    name: str = Field(description="Product name")  # Missing ...
    price: int = Field(..., description="Price")   # Should be float for money
    stock: str = Field("10")                       # Should be int for quantity
```

**Answers:**
```python
class Product(BaseModel):
    name: str = Field(..., description="Product name")     # Added ...
    price: float = Field(..., description="Price")         # Changed to float
    stock: int = Field(10, description="Stock quantity")   # Changed to int
```

---

## 🎯 Summary

**What we learned:**
1. ✅ Pydantic validates data automatically
2. ✅ Classes are blueprints/templates
3. ✅ Type hints specify what type of data to expect
4. ✅ Optional means "not required"
5. ✅ Field() adds validation rules
6. ✅ None means "empty/nothing"
7. ✅ Inheritance copies features from parent class

**Why it matters:**
- Prevents bugs from bad data
- Makes code self-documenting
- Catches errors early
- Enables auto-generated API docs

**Next steps:**
1. Read `src/schemas_explained.py` for detailed comments
2. Look at `src/database.py` to see how schemas work with database
3. Check `src/main.py` to see schemas in action with FastAPI

---

**Remember:** Don't worry if it doesn't all click immediately. These concepts take time to understand. Keep experimenting and asking questions!
