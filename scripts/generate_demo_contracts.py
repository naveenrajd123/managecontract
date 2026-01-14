"""
Generate 60-70 demo contract files covering all combinations of status and risk levels.
Filenames clearly indicate the combination for easy testing.
"""

import os
from datetime import datetime, timedelta
import random

# Create demo_contracts directory
output_dir = "demo_contracts"
os.makedirs(output_dir, exist_ok=True)

# Contract templates
PARTIES_A = ["TechCorp Solutions", "Global Dynamics Inc", "Acme Corporation", "MegaSoft Ltd", "InnovateTech Inc"]
PARTIES_B = [
    "DataVault Systems", "CloudNet Services", "SecureHost Inc", "FastShip Logistics",
    "BuildPro Construction", "MediaMax Agency", "LegalEase LLC", "FinanceFirst Bank",
    "HealthTech Medical", "EduSmart Academy", "RetailGiant Corp", "AutoParts Warehouse",
    "FoodService Distributors", "GreenEnergy Solutions", "TravelHub International",
    "InsureTech Group", "PropertyPro Realty", "ManuFact Industries", "ConsultPro Services",
    "DataCore Analytics", "CyberShield Security", "NextGen Robotics", "SmartHome Devices"
]

CONTRACT_TYPES = [
    "Software Licensing Agreement", "Service Level Agreement", "Equipment Lease",
    "Consulting Services Agreement", "Maintenance Contract", "Subscription Agreement",
    "Partnership Agreement", "Distribution Agreement", "Supply Agreement",
    "Cloud Services Agreement", "Professional Services Contract", "Marketing Services Agreement",
    "IT Support Contract", "Office Lease Agreement", "Equipment Rental Agreement",
    "Development Agreement", "API Integration License", "Data Processing Agreement",
    "Vendor Agreement", "Construction Contract", "Manufacturing Agreement", "Logistics Contract"
]

# Define combinations: (status, risk, count)
combinations = [
    # Active contracts - most common
    ("active", "low", 8),
    ("active", "medium", 10),
    ("active", "high", 6),
    ("active", "critical", 3),
    
    # Expired contracts
    ("expired", "low", 3),
    ("expired", "medium", 4),
    ("expired", "high", 2),
    ("expired", "critical", 1),
    
    # Renewed contracts
    ("renewed", "low", 2),
    ("renewed", "medium", 3),
    ("renewed", "high", 2),
    ("renewed", "critical", 1),
    
    # Pending contracts
    ("pending", "low", 3),
    ("pending", "medium", 4),
    ("pending", "high", 2),
    ("pending", "critical", 1),
    
    # Warning contracts - need attention!
    ("warning", "low", 2),
    ("warning", "medium", 3),
    ("warning", "high", 3),
    ("warning", "critical", 2),
]

def generate_contract_content(contract_num, status, risk, contract_type, party_a, party_b):
    """Generate realistic contract content."""
    
    now = datetime.now()
    
    # Set dates based on status
    if status == "expired":
        end_date = now - timedelta(days=random.randint(1, 90))
        start_date = end_date - timedelta(days=random.randint(365, 1095))
    elif status == "warning":
        end_date = now + timedelta(days=random.randint(5, 60))  # Expiring soon
        start_date = now - timedelta(days=random.randint(180, 730))
    elif status == "pending":
        start_date = now + timedelta(days=random.randint(1, 60))
        end_date = start_date + timedelta(days=random.randint(365, 1095))
    elif status == "renewed":
        start_date = now - timedelta(days=random.randint(1, 90))
        end_date = now + timedelta(days=random.randint(730, 1825))
    else:  # active
        start_date = now - timedelta(days=random.randint(90, 730))
        end_date = now + timedelta(days=random.randint(180, 1095))
    
    # Set contract value based on risk level
    if risk == "critical":
        value = random.randint(1000000, 5000000)
        penalties = random.randint(100000, 500000)
    elif risk == "high":
        value = random.randint(250000, 1000000)
        penalties = random.randint(25000, 100000)
    elif risk == "medium":
        value = random.randint(50000, 250000)
        penalties = random.randint(5000, 25000)
    else:  # low
        value = random.randint(5000, 50000)
        penalties = random.randint(500, 5000)
    
    # Payment terms based on risk
    payment_terms = {
        "critical": "Monthly, Net 15 days with automatic penalties",
        "high": "Quarterly, Net 30 days",
        "medium": "Monthly, Net 30 days",
        "low": "Upon receipt"
    }
    
    # SLA requirements
    sla_requirements = {
        "critical": "99.99% uptime, 24/7 support, 1-hour response time",
        "high": "99.9% uptime, business hours support, 4-hour response time",
        "medium": "99.5% uptime, business hours support, next business day response",
        "low": "Best effort, email support only"
    }
    
    contract_content = f"""
CONTRACT AGREEMENT
{contract_type.upper()}

Contract Number: CNT-2024-{contract_num:04d}
Date of Agreement: {start_date.strftime('%B %d, %Y')}

PARTIES TO THE AGREEMENT:

Party A (The Company): {party_a}
Address: 123 Business Street, Tech City, TC 12345
Email: contracts@{party_a.lower().replace(' ', '')}.com

Party B (The Vendor/Client): {party_b}
Address: 456 Commerce Avenue, Business District, BD 67890
Email: legal@{party_b.lower().replace(' ', '')}.com

WHEREAS, the parties wish to enter into this {contract_type} under the following terms and conditions:

1. SCOPE OF SERVICES
   {party_b} shall provide {contract_type.lower()} services to {party_a} as detailed in Appendix A.
   This includes but is not limited to professional consultation, implementation, maintenance, and support services.

2. CONTRACT TERM
   Start Date: {start_date.strftime('%B %d, %Y')}
   End Date: {end_date.strftime('%B %d, %Y')}
   Contract Duration: {(end_date - start_date).days} days
   
   Status: {status.upper()}
   Risk Classification: {risk.upper()}

3. FINANCIAL TERMS
   Total Contract Value: ${value:,} USD
   Payment Terms: {payment_terms[risk]}
   Currency: United States Dollars (USD)
   
   Payment Schedule:
   - Initial Payment: {random.randint(20, 40)}% upon contract signing
   - Milestone Payments: {random.randint(40, 60)}% upon completion of deliverables
   - Final Payment: {random.randint(10, 30)}% upon project acceptance

4. PAYMENT OBLIGATIONS
   All payments shall be made via wire transfer to the account specified by {party_b}.
   Late payments will incur a penalty of {random.randint(1, 3)}% per month.
   Invoice disputes must be raised within {random.randint(5, 15)} business days.

5. SERVICE LEVEL AGREEMENT (SLA)
   {sla_requirements[risk]}
   
   Penalties for SLA Breaches:
   - Each breach: ${penalties:,} or {random.randint(5, 15)}% of monthly fees, whichever is greater
   - Repeated breaches may result in contract termination

6. KEY DATES AND MILESTONES
   - Contract Effective Date: {start_date.strftime('%B %d, %Y')}
   - First Milestone: {(start_date + timedelta(days=30)).strftime('%B %d, %Y')}
   - Mid-Point Review: {(start_date + timedelta(days=(end_date-start_date).days//2)).strftime('%B %d, %Y')}
   - Final Deliverable: {(end_date - timedelta(days=30)).strftime('%B %d, %Y')}
   - Contract Expiration: {end_date.strftime('%B %d, %Y')}

7. TERMINATION CLAUSES
   Either party may terminate this agreement under the following conditions:
   
   a) Termination for Convenience:
      - {random.randint(30, 90)} days written notice required
      - Termination fee: {random.randint(10, 30)}% of remaining contract value
   
   b) Termination for Cause:
      - Immediate termination upon material breach
      - {random.randint(15, 30)} days to cure breach after written notice
      - No termination fee if other party is at fault
   
   c) Force Majeure:
      - Contract may be suspended during uncontrollable events
      - Extension of deadlines without penalties

8. LIABILITY AND INDEMNIFICATION
   Total Liability Cap: ${value * random.randint(2, 5):,} USD
   
   {party_b} agrees to indemnify and hold harmless {party_a} from:
   - Third-party claims arising from services provided
   - Intellectual property infringement claims
   - Data breaches or security incidents
   - Negligence or willful misconduct
   
   Exclusions:
   - Indirect, consequential, or punitive damages
   - Loss of profits or business opportunities
   - Claims arising from {party_a}'s actions or instructions

9. INTELLECTUAL PROPERTY RIGHTS
   - All work product becomes property of {party_a}
   - {party_b} retains rights to pre-existing materials and tools
   - Limited license granted for use of proprietary methodologies
   - Confidentiality obligations survive contract termination

10. CONFIDENTIALITY
    Both parties agree to maintain confidentiality of:
    - Proprietary business information
    - Technical specifications and trade secrets
    - Financial information and pricing
    - Customer data and business strategies
    
    Confidentiality period: {random.randint(2, 5)} years post-termination

11. INSURANCE REQUIREMENTS
    {party_b} must maintain the following insurance:
    - General Liability: ${random.randint(1, 5)}M minimum
    - Professional Liability: ${random.randint(1, 3)}M minimum
    - Cyber Liability: ${random.randint(500000, 2000000)} minimum
    - Workers Compensation: As required by law

12. COMPLIANCE AND REGULATORY
    Both parties shall comply with:
    - All applicable federal, state, and local laws
    - Industry-specific regulations (GDPR, HIPAA, SOC 2, etc.)
    - Data protection and privacy requirements
    - Export control and sanctions regulations

13. DISPUTE RESOLUTION
    - Initial negotiation period: {random.randint(15, 30)} days
    - Mediation: If negotiation fails
    - Binding Arbitration: Final resolution method
    - Venue: {random.choice(['New York', 'Delaware', 'California'])}

14. AMENDMENT AND MODIFICATION
    This contract may only be modified by written agreement signed by both parties.
    Change requests must be submitted in writing with {random.randint(10, 30)} days notice.

15. GOVERNING LAW
    This agreement shall be governed by the laws of the State of {random.choice(['New York', 'Delaware', 'California'])},
    without regard to its conflict of law provisions.

16. ENTIRE AGREEMENT
    This contract represents the entire agreement between the parties and supersedes
    all prior negotiations, representations, or agreements, whether written or oral.

SIGNATURES:

For {party_a}:
_________________________________
Name: {random.choice(['John Smith', 'Sarah Johnson', 'Michael Chen', 'Emily Davis'])}
Title: {random.choice(['CEO', 'CFO', 'VP of Operations', 'General Counsel'])}
Date: {start_date.strftime('%B %d, %Y')}

For {party_b}:
_________________________________
Name: {random.choice(['David Wilson', 'Lisa Martinez', 'Robert Taylor', 'Jennifer Brown'])}
Title: {random.choice(['President', 'Managing Director', 'VP of Sales', 'Legal Director'])}
Date: {start_date.strftime('%B %d, %Y')}

--- END OF CONTRACT ---

APPENDIX A: DETAILED SCOPE OF WORK
[Detailed technical specifications and deliverables would be listed here]

APPENDIX B: PRICING SCHEDULE
[Detailed breakdown of costs and payment milestones would be listed here]

APPENDIX C: SERVICE LEVEL AGREEMENT (SLA) METRICS
[Specific performance metrics and measurement criteria would be listed here]

Contract Status: {status.upper()}
Risk Level: {risk.upper()}
Generated for demo purposes.
"""
    
    return contract_content

# Generate all contracts
contract_counter = 1
total_contracts = 0

print("Generating demo contract files...")
print("=" * 60)

for status, risk, count in combinations:
    print(f"\nGenerating {count} {status.upper()} contracts with {risk.upper()} risk...")
    
    for i in range(count):
        contract_type = random.choice(CONTRACT_TYPES)
        party_a = random.choice(PARTIES_A)
        party_b = random.choice(PARTIES_B)
        
        filename = f"CNT-2024-{contract_counter:04d}_{status.upper()}_{risk.upper()}_{contract_type.replace(' ', '_')}.txt"
        filepath = os.path.join(output_dir, filename)
        
        content = generate_contract_content(contract_counter, status, risk, contract_type, party_a, party_b)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  [OK] Created: {filename}")
        contract_counter += 1
        total_contracts += 1

print("\n" + "=" * 60)
print(f"[SUCCESS] Successfully generated {total_contracts} demo contract files!")
print(f"[LOCATION] {os.path.abspath(output_dir)}/")
print("\n" + "=" * 60)
print("\nDistribution Summary:")
print(f"  Active:   {sum(c for s, r, c in combinations if s == 'active')} contracts")
print(f"  Expired:  {sum(c for s, r, c in combinations if s == 'expired')} contracts")
print(f"  Renewed:  {sum(c for s, r, c in combinations if s == 'renewed')} contracts")
print(f"  Pending:  {sum(c for s, r, c in combinations if s == 'pending')} contracts")
print(f"  Warning:  {sum(c for s, r, c in combinations if s == 'warning')} contracts")
print("\n  Low Risk:      {sum(c for s, r, c in combinations if r == 'low')} contracts")
print(f"  Medium Risk:   {sum(c for s, r, c in combinations if r == 'medium')} contracts")
print(f"  High Risk:     {sum(c for s, r, c in combinations if r == 'high')} contracts")
print(f"  Critical Risk: {sum(c for s, r, c in combinations if r == 'critical')} contracts")
print("\n" + "=" * 60)
print("\n[READY] Ready for testing! Upload these files to see the dashboard in action!")
