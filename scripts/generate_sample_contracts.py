"""
Contract Generator Script
Automatically generates realistic sample contracts with various scenarios.

This creates contracts with different:
- Types (Software, Consulting, Maintenance, etc.)
- Statuses (Active, Expired, Terminated, Renewed)
- Risk levels (Low, Medium, High, Critical)
- Financial values
- Expiration scenarios
- Legal clauses and penalties
"""

import random
import os
from datetime import datetime, timedelta
from typing import List, Dict

# Contract templates and variations
CONTRACT_TYPES = [
    "Software License Agreement",
    "Professional Services Agreement",
    "Maintenance and Support Agreement",
    "Consulting Services Agreement",
    "Master Service Agreement",
    "Equipment Lease Agreement",
    "Cloud Services Agreement",
    "IT Support Agreement",
    "Data Processing Agreement",
    "Partnership Agreement"
]

COMPANIES = [
    "TechCorp Solutions Inc.",
    "Global Innovations Ltd.",
    "Digital Ventures LLC",
    "Enterprise Systems Group",
    "Advanced Technologies Co.",
    "Strategic Partners International",
    "Innovation Labs Corporation",
    "Future Tech Industries",
    "Smart Solutions Provider",
    "NextGen Services Ltd."
]

VENDORS = [
    "Acme Software Corporation",
    "Premier Consulting Group",
    "Elite Technology Partners",
    "Professional Services Inc.",
    "Quality Solutions Provider",
    "Excellent Systems Ltd.",
    "Superior Tech Services",
    "Advanced Solutions Corp.",
    "Prime Technologies LLC",
    "Best-in-Class Services"
]

# Payment terms variations
PAYMENT_TERMS = [
    {"amount": 50000, "frequency": "annually", "due_days": 30},
    {"amount": 125000, "frequency": "annually", "due_days": 45},
    {"amount": 25000, "frequency": "quarterly", "due_days": 15},
    {"amount": 10000, "frequency": "monthly", "due_days": 30},
    {"amount": 200000, "frequency": "annually", "due_days": 60},
    {"amount": 75000, "frequency": "semi-annually", "due_days": 30},
]

# Penalty clauses
PENALTIES = [
    "Late payment penalty of 2% per month on outstanding amounts",
    "Service level breach penalty of $5,000 per incident",
    "Delay penalty of $1,000 per day for missed deadlines",
    "Non-compliance penalty up to 10% of contract value",
    "Security breach penalty of $50,000 per occurrence",
    "Early termination penalty of 25% of remaining contract value"
]

# Termination clauses
TERMINATION_CLAUSES = [
    "Either party may terminate with 90 days written notice",
    "Immediate termination allowed for material breach",
    "30 days notice required for termination without cause",
    "Termination requires 60 days notice and settlement of outstanding amounts",
    "No early termination allowed except for cause with 14 days cure period",
    "Either party may terminate with 120 days notice after initial term"
]

# Legal clauses
LEGAL_CLAUSES = [
    "Governed by the laws of the State of California",
    "Subject to arbitration in New York, NY",
    "Disputes resolved through mediation before litigation",
    "Jurisdiction: Delaware Court of Chancery",
    "Governed by English law with London jurisdiction",
    "Subject to Federal arbitration rules"
]

# Confidentiality terms
CONFIDENTIALITY = [
    "All information marked 'Confidential' must be protected for 5 years",
    "Non-disclosure requirements survive contract termination indefinitely",
    "Confidential information protected during term and 3 years after",
    "Standard NDA provisions apply with 7-year protection period",
    "Two-way confidentiality with exceptions for public information"
]

# Liability limitations
LIABILITY_TERMS = [
    "Liability capped at 12 months of fees paid",
    "Maximum liability limited to contract value",
    "Unlimited liability for gross negligence or willful misconduct",
    "Liability limited to $500,000 except for IP infringement",
    "No limitation on liability for data breaches",
    "Consequential damages excluded, direct damages capped at annual fees"
]


def generate_contract_text(
    contract_type: str,
    company: str,
    vendor: str,
    contract_number: str,
    start_date: datetime,
    end_date: datetime,
    payment: Dict,
    status: str,
    has_penalties: bool,
    has_early_termination: bool,
    risk_level: str,
    pages: int = 20
) -> str:
    """Generate realistic contract text with specified parameters."""
    
    # Select random clauses
    penalty_clause = random.choice(PENALTIES) if has_penalties else "No penalty clauses specified"
    termination = random.choice(TERMINATION_CLAUSES)
    legal_clause = random.choice(LEGAL_CLAUSES)
    confidentiality = random.choice(CONFIDENTIALITY)
    liability = random.choice(LIABILITY_TERMS)
    
    # Calculate some dates
    execution_date = start_date - timedelta(days=random.randint(7, 30))
    
    # Build contract content
    contract = f"""
{contract_type.upper()}

Contract Number: {contract_number}
Effective Date: {start_date.strftime('%B %d, %Y')}
Execution Date: {execution_date.strftime('%B %d, %Y')}

================================================================================
PARTIES TO THIS AGREEMENT
================================================================================

This {contract_type} ("Agreement") is entered into on {execution_date.strftime('%B %d, %Y')}
("Effective Date") by and between:

PARTY A: {company}
Address: 1234 Business Park Drive, Suite 500
City: San Francisco, State: CA, Zip: 94102
("Client" or "Company")

AND

PARTY B: {vendor}
Address: 5678 Commerce Boulevard, Floor 3
City: New York, State: NY, Zip: 10001
("Vendor" or "Service Provider")

Collectively referred to as the "Parties" and individually as a "Party."

================================================================================
RECITALS
================================================================================

WHEREAS, Company requires professional services and solutions in connection with
its business operations and strategic initiatives;

WHEREAS, Vendor represents that it has the necessary expertise, experience, and
resources to provide such services;

WHEREAS, the Parties wish to establish the terms and conditions under which
Vendor shall provide services to Company;

NOW, THEREFORE, in consideration of the mutual covenants and agreements contained
herein, and for other good and valuable consideration, the receipt and sufficiency
of which are hereby acknowledged, the Parties agree as follows:

================================================================================
ARTICLE 1: DEFINITIONS
================================================================================

1.1 "Agreement" means this {contract_type} including all exhibits and amendments.

1.2 "Services" means all professional services, deliverables, and work products
to be provided by Vendor under this Agreement as described in the Statement of Work.

1.3 "Confidential Information" means any non-public information disclosed by one
Party to the other, including but not limited to business plans, technical data,
customer information, and financial data.

1.4 "Intellectual Property" means all patents, copyrights, trademarks, trade secrets,
and other proprietary rights.

1.5 "Deliverables" means all work products, documentation, and materials to be
provided by Vendor to Company.

1.6 "Force Majeure" means any event beyond the reasonable control of a Party,
including acts of God, war, terrorism, strikes, or government actions.

================================================================================
ARTICLE 2: SCOPE OF SERVICES
================================================================================

2.1 Services Overview
Vendor agrees to provide the following services to Company:

a) Primary Services: Comprehensive professional services as detailed in the
   attached Statement of Work, including but not limited to:
   - Strategic consulting and advisory services
   - Technical implementation and deployment
   - Ongoing support and maintenance
   - Training and knowledge transfer
   - Documentation and reporting

b) Service Levels: Vendor shall maintain service levels as specified in the
   Service Level Agreement (SLA) attached as Exhibit A.

c) Resources: Vendor shall assign qualified personnel with appropriate skills
   and experience to perform the Services.

2.2 Service Standards
All Services shall be performed:
- In a professional and workmanlike manner
- In accordance with industry best practices
- In compliance with all applicable laws and regulations
- Using qualified and experienced personnel
- Within the timelines specified in project schedules

2.3 Change Management
Any changes to the scope of Services shall be documented in a written Change
Order signed by both Parties, specifying the nature of the change, impact on
timeline, and any adjustment to fees.

================================================================================
ARTICLE 3: TERM AND TERMINATION
================================================================================

3.1 Initial Term
This Agreement shall commence on {start_date.strftime('%B %d, %Y')} and continue
until {end_date.strftime('%B %d, %Y')} ("Initial Term"), unless earlier terminated
in accordance with this Article.

3.2 Renewal Term
{"This Agreement shall automatically renew for successive one-year periods unless either Party provides written notice of non-renewal at least 90 days before the end of the then-current term." if status in ["active", "renewed"] else "This Agreement does not include automatic renewal provisions."}

3.3 Termination for Convenience
{termination}

3.4 Termination for Cause
Either Party may terminate this Agreement immediately upon written notice if:
a) The other Party materially breaches this Agreement and fails to cure within 30 days
b) The other Party becomes insolvent or files for bankruptcy
c) The other Party's license to operate is suspended or revoked

{"3.5 Early Termination" if has_early_termination else ""}
{"In the event of early termination by Company without cause, Company shall pay Vendor 50% of the remaining fees for the term. If terminated by Vendor without cause, Vendor shall refund 25% of fees paid for the current period." if has_early_termination else ""}

3.6 Effect of Termination
Upon termination:
a) All outstanding fees shall become immediately due
b) Vendor shall deliver all completed work and Deliverables
c) Each Party shall return or destroy Confidential Information
d) Provisions intended to survive shall remain in effect

================================================================================
ARTICLE 4: FEES AND PAYMENT TERMS
================================================================================

4.1 Service Fees
Company shall pay Vendor the following fees for Services:

Total Contract Value: ${payment['amount']:,} USD per {payment['frequency']}
Payment Structure: {payment['frequency'].capitalize()} invoicing
Invoice Due: Net {payment['due_days']} days from invoice date

4.2 Payment Schedule
Invoices shall be submitted {payment['frequency']} and shall include:
- Detailed description of services provided
- Hours worked (if applicable)
- Expenses incurred (if reimbursable)
- Applicable taxes

4.3 Late Payment
{"Payment not received within " + str(payment['due_days']) + " days shall accrue interest at 1.5% per month." if not has_penalties else penalty_clause}

4.4 Expenses
{"Vendor shall be reimbursed for pre-approved, reasonable expenses incurred in connection with providing Services, subject to Company's expense policy and documentation requirements." if random.choice([True, False]) else "All expenses are included in the fees and no additional reimbursement shall be provided."}

4.5 Taxes
All fees are exclusive of applicable taxes. Company shall be responsible for all
sales, use, and other taxes except for taxes based on Vendor's income.

================================================================================
ARTICLE 5: INTELLECTUAL PROPERTY RIGHTS
================================================================================

5.1 Ownership of Deliverables
All Deliverables created specifically for Company under this Agreement shall be
considered "work made for hire" and shall be the sole property of Company.

5.2 Pre-Existing Materials
Vendor retains all rights to its pre-existing materials, methodologies, and
tools. Company receives a non-exclusive license to use such materials solely
in connection with the Deliverables.

5.3 License Grant
Vendor grants Company a perpetual, worldwide, non-exclusive, royalty-free license
to use, modify, and distribute the Deliverables for Company's internal business
purposes.

5.4 Third-Party Materials
Vendor warrants that all third-party materials included in Deliverables are
properly licensed and will not infringe any third-party rights.

================================================================================
ARTICLE 6: CONFIDENTIALITY AND DATA PROTECTION
================================================================================

6.1 Confidentiality Obligations
{confidentiality}

6.2 Exceptions
Confidential Information does not include information that:
a) Is publicly available through no breach of this Agreement
b) Was rightfully known prior to disclosure
c) Is independently developed without use of Confidential Information
d) Is required to be disclosed by law or court order

6.3 Data Protection
Vendor shall comply with all applicable data protection laws including GDPR,
CCPA, and other privacy regulations. Vendor shall implement appropriate
technical and organizational measures to protect personal data.

6.4 Security Requirements
Vendor shall maintain information security practices including:
- Access controls and authentication
- Encryption of data in transit and at rest
- Regular security assessments and updates
- Incident response procedures
- Employee training and background checks

================================================================================
ARTICLE 7: WARRANTIES AND REPRESENTATIONS
================================================================================

7.1 Mutual Warranties
Each Party warrants that:
a) It has full authority to enter into this Agreement
b) This Agreement does not conflict with other obligations
c) It will comply with all applicable laws

7.2 Vendor Warranties
Vendor warrants that:
a) Services will be performed in a professional manner
b) Services will conform to specifications and requirements
c) Deliverables will be free from defects for 90 days
d) It has all necessary licenses and permits
e) Services will not infringe third-party rights

7.3 Disclaimer
EXCEPT AS EXPRESSLY PROVIDED, VENDOR MAKES NO WARRANTIES, EXPRESS OR IMPLIED,
INCLUDING WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.

================================================================================
ARTICLE 8: LIMITATION OF LIABILITY
================================================================================

8.1 Limitation
{liability}

8.2 Exclusions
Neither Party shall be liable for indirect, incidental, consequential, special,
or punitive damages, including lost profits, even if advised of the possibility.

8.3 Exceptions
Limitations do not apply to:
a) Breach of confidentiality obligations
b) Intellectual property infringement
c) Gross negligence or willful misconduct
d) Indemnification obligations

================================================================================
ARTICLE 9: INDEMNIFICATION
================================================================================

9.1 Vendor Indemnification
Vendor shall indemnify and hold harmless Company from claims arising from:
a) Vendor's negligence or willful misconduct
b) Vendor's breach of this Agreement
c) Infringement of third-party intellectual property rights
d) Violation of applicable laws by Vendor

9.2 Company Indemnification
Company shall indemnify Vendor from claims arising from:
a) Company's breach of this Agreement
b) Misuse of Deliverables by Company
c) Infringement based on Company's specifications

9.3 Indemnification Procedures
The indemnified Party shall:
a) Promptly notify the indemnifying Party of claims
b) Allow the indemnifying Party to control defense
c) Cooperate in the defense of claims

================================================================================
ARTICLE 10: INSURANCE
================================================================================

10.1 Required Coverage
Vendor shall maintain the following insurance:
a) Commercial General Liability: $2,000,000 per occurrence
b) Professional Liability: $1,000,000 per claim
c) Workers' Compensation: Statutory limits
d) Cyber Liability: $1,000,000 per occurrence

10.2 Evidence of Insurance
Vendor shall provide certificates of insurance upon request naming Company
as additional insured.

================================================================================
ARTICLE 11: COMPLIANCE AND AUDIT RIGHTS
================================================================================

11.1 Regulatory Compliance
Vendor shall comply with all applicable laws, regulations, and industry standards,
including but not limited to:
- Employment and labor laws
- Environmental regulations
- Export control laws
- Anti-corruption laws (FCPA, UK Bribery Act)
- Industry-specific regulations

11.2 Audit Rights
Company may audit Vendor's compliance with this Agreement upon reasonable notice.
Vendor shall cooperate and provide requested documentation. If audit reveals
material non-compliance, Vendor shall bear audit costs.

11.3 Quality Assurance
Company may conduct quality assurance reviews of Services and Deliverables.
Vendor shall remediate any deficiencies identified.

================================================================================
ARTICLE 12: DISPUTE RESOLUTION
================================================================================

12.1 Negotiation
The Parties shall first attempt to resolve disputes through good faith negotiation
between senior executives.

12.2 Mediation
If negotiation fails within 30 days, disputes shall be submitted to mediation
under the rules of the American Arbitration Association.

12.3 Arbitration/Litigation
{legal_clause}

12.4 Equitable Relief
Nothing prevents either Party from seeking injunctive or equitable relief to
protect intellectual property or confidential information.

================================================================================
ARTICLE 13: GENERAL PROVISIONS
================================================================================

13.1 Independent Contractors
The Parties are independent contractors. Nothing creates a partnership, joint
venture, or employment relationship.

13.2 Assignment
Neither Party may assign this Agreement without prior written consent, except
to a successor in connection with a merger or acquisition.

13.3 Force Majeure
Neither Party shall be liable for delays caused by Force Majeure events beyond
their reasonable control.

13.4 Notices
All notices shall be in writing and delivered by email or certified mail to:

For Company: legal@{company.lower().replace(' ', '').replace('.', '')}.com
For Vendor: contracts@{vendor.lower().replace(' ', '').replace('.', '')}.com

13.5 Entire Agreement
This Agreement constitutes the entire agreement and supersedes all prior
negotiations and agreements.

13.6 Amendments
Amendments must be in writing and signed by authorized representatives of both Parties.

13.7 Severability
If any provision is found invalid, the remainder shall continue in effect.

13.8 Waiver
Failure to enforce any provision does not waive the right to enforce it later.

13.9 Counterparts
This Agreement may be executed in counterparts, each constituting an original.

13.10 Survival
Provisions intended to survive termination shall remain in effect, including
confidentiality, intellectual property, indemnification, and limitation of liability.

================================================================================
ARTICLE 14: SPECIAL PROVISIONS
================================================================================

14.1 Risk Assessment
This contract has been assessed as {risk_level.upper()} RISK based on:
- Contract value and payment terms
- Complexity of services
- Compliance requirements
- Liability exposure
- Historical vendor performance

{"14.2 Penalties and Liquidated Damages" if has_penalties else ""}
{penalty_clause if has_penalties else ""}

14.3 Service Level Agreement
Detailed service levels, performance metrics, and remedies for non-performance
are specified in Exhibit A - Service Level Agreement.

14.4 Security Requirements
Vendor shall comply with Company's information security policies and maintain
certifications including SOC 2, ISO 27001, or equivalent.

14.5 Subcontractors
Vendor may not use subcontractors without prior written approval. Vendor remains
fully responsible for all subcontractor performance.

14.6 Background Checks
All Vendor personnel with access to Company systems or data must pass background
checks meeting Company's standards.

14.7 Training Requirements
Vendor shall provide training to Company personnel on use of Deliverables and
systems.

14.8 Documentation
Vendor shall provide comprehensive documentation including user guides, technical
specifications, and operational procedures.

14.9 Transition Assistance
Upon expiration or termination, Vendor shall provide up to 30 days of transition
assistance to ensure continuity of services.

14.10 Benchmarking
Company reserves the right to conduct benchmarking assessments to ensure Vendor's
fees remain competitive with market rates.

"""

    # Add additional sections to reach desired page count
    additional_sections = [
        "\n================================================================================\n",
        "ARTICLE 15: OPERATIONAL PROCEDURES\n",
        "================================================================================\n\n",
        "15.1 Communication Protocols\n",
        "Regular status meetings shall be held weekly to review progress, issues, and upcoming milestones.\n",
        "Vendor shall provide monthly reports detailing services provided, metrics achieved, and any concerns.\n\n",
        "15.2 Change Control Process\n",
        "All changes must follow the established change control procedure including impact analysis,\n",
        "approval workflow, and documentation requirements.\n\n",
        "15.3 Escalation Procedures\n",
        "Issues shall be escalated according to severity: Critical (1 hour), High (4 hours), Medium (1 business day).\n\n",
        "15.4 Disaster Recovery\n",
        "Vendor shall maintain disaster recovery and business continuity plans with tested recovery\n",
        "time objectives (RTO) of 4 hours and recovery point objectives (RPO) of 1 hour.\n\n",
        "15.5 Performance Monitoring\n",
        "Key performance indicators shall be tracked and reported monthly, including availability,\n",
        "response times, error rates, and customer satisfaction scores.\n\n"
    ]
    
    # Repeat content to reach target pages (approximate)
    content_repetitions = max(1, pages // 5)
    for _ in range(content_repetitions):
        contract += "".join(additional_sections)
        contract += f"\n{'='*80}\n"
        contract += "APPENDIX: DETAILED SPECIFICATIONS AND REQUIREMENTS\n"
        contract += f"{'='*80}\n\n"
        contract += f"Technical specifications, detailed requirements, and implementation guidelines\n"
        contract += f"are provided in this appendix to ensure clarity and mutual understanding.\n\n"
    
    # Add signature block
    contract += f"""

================================================================================
SIGNATURE PAGE
================================================================================

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date
first written above.

{company}

By: _______________________________
Name: Sarah Johnson
Title: Chief Executive Officer
Date: {execution_date.strftime('%B %d, %Y')}


{vendor}

By: _______________________________
Name: Michael Chen
Title: President
Date: {execution_date.strftime('%B %d, %Y')}


EXHIBITS:
- Exhibit A: Service Level Agreement
- Exhibit B: Statement of Work
- Exhibit C: Pricing Schedule
- Exhibit D: Security Requirements
- Exhibit E: Compliance Certifications

END OF AGREEMENT
Contract Number: {contract_number}
Total Pages: {pages}
"""
    
    return contract


def generate_contract_scenarios(num_contracts: int = 50) -> List[Dict]:
    """Generate diverse contract scenarios."""
    
    scenarios = []
    current_date = datetime.now()
    
    for i in range(num_contracts):
        contract_num = f"CNT-2024-{i+1:03d}"
        
        # Randomize parameters for diversity
        contract_type = random.choice(CONTRACT_TYPES)
        company = random.choice(COMPANIES)
        vendor = random.choice(VENDORS)
        payment = random.choice(PAYMENT_TERMS)
        
        # Create different scenarios
        scenario_type = random.choice([
            "active_normal",
            "expiring_soon",
            "expired",
            "renewed",
            "early_terminated",
            "high_risk",
            "with_penalties"
        ])
        
        if scenario_type == "active_normal":
            start_date = current_date - timedelta(days=random.randint(180, 720))
            end_date = current_date + timedelta(days=random.randint(180, 720))
            status = "active"
            risk_level = random.choice(["low", "medium"])
            has_penalties = random.choice([True, False])
            has_early_termination = False
            
        elif scenario_type == "expiring_soon":
            start_date = current_date - timedelta(days=random.randint(300, 600))
            end_date = current_date + timedelta(days=random.randint(15, 89))  # Expires in 2-3 months
            status = "active"
            risk_level = random.choice(["medium", "high"])
            has_penalties = True
            has_early_termination = False
            
        elif scenario_type == "expired":
            start_date = current_date - timedelta(days=random.randint(400, 800))
            end_date = current_date - timedelta(days=random.randint(10, 90))
            status = "expired"
            risk_level = "high"
            has_penalties = True
            has_early_termination = False
            
        elif scenario_type == "renewed":
            start_date = current_date - timedelta(days=random.randint(400, 1000))
            end_date = current_date + timedelta(days=random.randint(365, 730))
            status = "renewed"
            risk_level = "low"
            has_penalties = False
            has_early_termination = False
            
        elif scenario_type == "early_terminated":
            start_date = current_date - timedelta(days=random.randint(200, 400))
            end_date = current_date - timedelta(days=random.randint(5, 30))
            status = "terminated"
            risk_level = "critical"
            has_penalties = True
            has_early_termination = True
            
        elif scenario_type == "high_risk":
            start_date = current_date - timedelta(days=random.randint(100, 300))
            end_date = current_date + timedelta(days=random.randint(30, 180))
            status = "active"
            risk_level = "critical"
            has_penalties = True
            has_early_termination = True
            
        else:  # with_penalties
            start_date = current_date - timedelta(days=random.randint(200, 500))
            end_date = current_date + timedelta(days=random.randint(90, 365))
            status = "active"
            risk_level = random.choice(["medium", "high"])
            has_penalties = True
            has_early_termination = False
        
        scenarios.append({
            "contract_number": contract_num,
            "contract_type": contract_type,
            "company": company,
            "vendor": vendor,
            "start_date": start_date,
            "end_date": end_date,
            "payment": payment,
            "status": status,
            "risk_level": risk_level,
            "has_penalties": has_penalties,
            "has_early_termination": has_early_termination,
            "pages": random.randint(15, 35)  # Varied page counts
        })
    
    return scenarios


def main():
    """Main function to generate contracts."""
    
    print("=" * 80)
    print("CONTRACT GENERATOR - Sample Data Creation")
    print("=" * 80)
    print()
    
    # Ask user for number of contracts
    try:
        num_contracts = int(input("How many contracts to generate? (default 50): ") or "50")
    except:
        num_contracts = 50
    
    # Ask for page range
    try:
        pages = int(input("Approximate pages per contract? (default 20): ") or "20")
    except:
        pages = 20
    
    print()
    print(f"Generating {num_contracts} contracts with ~{pages} pages each...")
    print()
    
    # Generate scenarios
    scenarios = generate_contract_scenarios(num_contracts)
    
    # Create contracts
    created_files = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"[{i}/{num_contracts}] Creating {scenario['contract_number']}...", end=" ")
        
        # Generate contract text
        contract_text = generate_contract_text(
            contract_type=scenario['contract_type'],
            company=scenario['company'],
            vendor=scenario['vendor'],
            contract_number=scenario['contract_number'],
            start_date=scenario['start_date'],
            end_date=scenario['end_date'],
            payment=scenario['payment'],
            status=scenario['status'],
            has_penalties=scenario['has_penalties'],
            has_early_termination=scenario['has_early_termination'],
            risk_level=scenario['risk_level'],
            pages=pages
        )
        
        # Save to file
        filename = f"data/contracts/{scenario['contract_number']}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(contract_text)
        
        created_files.append({
            "filename": filename,
            "contract_number": scenario['contract_number'],
            "type": scenario['contract_type'],
            "status": scenario['status'],
            "risk": scenario['risk_level'],
            "value": scenario['payment']['amount'],
            "start": scenario['start_date'].strftime('%Y-%m-%d'),
            "end": scenario['end_date'].strftime('%Y-%m-%d')
        })
        
        print(f"[OK] ({scenario['status']}, {scenario['risk_level']} risk)")
    
    print()
    print("=" * 80)
    print(f"[SUCCESS] Created {len(created_files)} contracts!")
    print("=" * 80)
    print()
    
    # Print summary statistics
    statuses = {}
    risks = {}
    for contract in created_files:
        statuses[contract['status']] = statuses.get(contract['status'], 0) + 1
        risks[contract['risk']] = risks.get(contract['risk'], 0) + 1
    
    print("[SUMMARY]")
    print(f"   Total Contracts: {len(created_files)}")
    print()
    print("   By Status:")
    for status, count in statuses.items():
        print(f"   - {status.capitalize()}: {count}")
    print()
    print("   By Risk Level:")
    for risk, count in risks.items():
        print(f"   - {risk.capitalize()}: {count}")
    print()
    
    # Save metadata
    import json
    with open('data/contracts_metadata.json', 'w') as f:
        json.dump(created_files, f, indent=2)
    
    print("[SAVED] Metadata saved to: data/contracts_metadata.json")
    print()
    print("[NEXT STEPS]")
    print("   1. Run: python upload_contracts_to_db.py")
    print("   2. Check dashboard at http://localhost:8000")
    print()


if __name__ == "__main__":
    main()
