"""
Generate Balanced Demo Contracts with Compliance Factors
Creates contracts with appropriate financial values AND compliance risk escalators
"""

import os
import random
from datetime import datetime, timedelta
from pathlib import Path

# Risk profiles with compliance factors
RISK_PROFILES = {
    'LOW': {
        'contract_value_range': (5000, 24000),
        'liability_multiplier': (2, 3),
        'sla_penalty_range': (100, 490),
        'termination_fee_percent': (5, 9),
        'notice_days_range': (30, 44),
        'late_payment_percent': (1, 2),
        'insurance': {'general': '1M', 'professional': '500K', 'cyber_range': (100000, 240000)},
        'cure_days': (10, 14),
        'confidentiality_years': (1, 2),
        'dispute_days': (10, 14),
        'change_notice_days': (14, 20),
        'compliance_factors': [],  # No major compliance requirements
        'description': 'Low financial risk, no major compliance requirements'
    },
    'MEDIUM': {
        'contract_value_range': (25000, 99000),
        'liability_multiplier': (3, 4),
        'sla_penalty_range': (500, 1900),
        'termination_fee_percent': (10, 19),
        'notice_days_range': (45, 59),
        'late_payment_percent': (2, 3),
        'insurance': {'general': '2M', 'professional': '1M', 'cyber_range': (250000, 490000)},
        'cure_days': (15, 19),
        'confidentiality_years': (2, 3),
        'dispute_days': (15, 19),
        'change_notice_days': (21, 27),
        'compliance_factors': ['Standard data protection', 'Industry best practices'],
        'description': 'Medium financial risk, standard compliance'
    },
    'HIGH': {
        'contract_value_range': (100000, 499000),
        'liability_multiplier': (4, 5),
        'sla_penalty_range': (2000, 9900),
        'termination_fee_percent': (20, 29),
        'notice_days_range': (60, 89),
        'late_payment_percent': (3, 5),
        'insurance': {'general': '5M', 'professional': '3M', 'cyber_range': (500000, 990000)},
        'cure_days': (20, 29),
        'confidentiality_years': (3, 5),
        'dispute_days': (20, 29),
        'change_notice_days': (28, 44),
        'compliance_factors': ['GDPR compliance required', 'PCI-DSS Level 1', 'SOC 2 Type II certification'],
        'description': 'High financial risk + regulatory compliance requirements'
    },
    'CRITICAL': {
        'contract_value_range': (500000, 1900000),
        'liability_multiplier': (5, 8),
        'sla_penalty_range': (10000, 49000),
        'termination_fee_percent': (30, 49),
        'notice_days_range': (90, 119),
        'late_payment_percent': (5, 8),
        'insurance': {'general': '10M', 'professional': '5M', 'cyber_range': (1000000, 4900000)},
        'cure_days': (30, 44),
        'confidentiality_years': (5, 7),
        'dispute_days': (30, 44),
        'change_notice_days': (45, 59),
        'compliance_factors': [
            'HIPAA compliance mandatory',
            'GDPR with substantial data processing',
            'FDA regulations',
            'SOX financial reporting requirements',
            'Export control (ITAR/EAR)',
            'Critical infrastructure protection'
        ],
        'description': 'Critical financial risk + major regulatory requirements'
    }
}

COMPLIANCE_DETAILS = {
    'LOW': """
12. COMPLIANCE AND REGULATORY
    Both parties shall comply with:
    - All applicable federal, state, and local laws
    - General business regulations
    - Standard data protection practices
    - Anti-corruption and ethics policies
    """,
    'MEDIUM': """
12. COMPLIANCE AND REGULATORY
    Both parties shall comply with:
    - All applicable federal, state, and local laws
    - Industry-specific regulations and standards
    - Data protection best practices (encryption, access controls)
    - Privacy policies and customer data handling
    - Information security standards (ISO 27001 recommended)
    - Anti-corruption and ethics policies
    
    Standard Compliance Requirements:
    - Annual compliance attestation
    - Quarterly security reviews
    - Incident reporting within 48 hours
    """,
    'HIGH': """
12. COMPLIANCE AND REGULATORY
    Both parties shall comply with:
    - All applicable federal, state, and local laws
    - GDPR (General Data Protection Regulation) - Full compliance required
    - PCI-DSS Level 1 - Payment card data security standards
    - SOC 2 Type II certification - Annual audit required
    - ISO 27001 Information Security Management
    - Privacy Shield Framework (if applicable)
    - State privacy laws (CCPA, CPRA, etc.)
    - Anti-corruption and ethics policies (FCPA, UK Bribery Act)
    
    Enhanced Compliance Requirements:
    - Quarterly third-party security audits
    - Annual penetration testing
    - Data Protection Impact Assessments (DPIA)
    - Breach notification within 72 hours
    - Right to audit upon 30 days notice
    - Data Processing Agreements (DPA) required
    - Appointment of Data Protection Officer (DPO)
    
    RISK ESCALATORS (Increase from Medium to High):
    + GDPR compliance with personal data processing
    + PCI-DSS requirements for payment systems
    + SOC 2 Type II audit obligations
    """,
    'CRITICAL': """
12. COMPLIANCE AND REGULATORY
    Both parties shall comply with:
    - All applicable federal, state, and local laws
    - HIPAA (Health Insurance Portability and Accountability Act)
    - Protected Health Information (PHI) handling requirements
    - HITECH Act - Security and breach notification
    - GDPR with extensive personal data processing
    - FDA regulations for medical devices/software
    - SOX (Sarbanes-Oxley) financial reporting requirements
    - PCI-DSS Level 1 - Payment card industry standards
    - Export control regulations (ITAR, EAR)
    - Critical infrastructure protection (NERC CIP, FISMA)
    - State privacy laws (CCPA, CPRA, HIPAA state laws)
    - FedRAMP compliance (if government contract)
    - ISO 27001, ISO 13485 (medical devices)
    - Anti-corruption (FCPA, UK Bribery Act, local laws)
    
    Critical Compliance Requirements:
    - Continuous third-party security monitoring
    - Monthly penetration testing and vulnerability assessments
    - Business Associate Agreement (BAA) for HIPAA
    - Data Processing Agreements (DPA) with strict terms
    - Mandatory Data Protection Officer (DPO) and compliance officer
    - Breach notification within 24 hours to all parties
    - Right to audit at any time with 24-hour notice
    - Annual regulatory audits (FDA, HHS, etc.)
    - Incident response plan with 1-hour response time
    - Disaster recovery and business continuity testing quarterly
    - Encryption at rest and in transit (FIPS 140-2 compliant)
    - Multi-factor authentication (MFA) mandatory
    - Role-based access controls (RBAC) with least privilege
    
    RISK ESCALATORS (Increase from High to Critical):
    + HIPAA/PHI handling - Protected health information
    + FDA medical device regulations
    + SOX financial reporting obligations
    + Export controls (ITAR/EAR) - National security
    + Critical infrastructure protection requirements
    + Handles sensitive personal data at scale (>100K records)
    
    Regulatory Penalties:
    - HIPAA violations: Up to $1.5M per year per violation type
    - GDPR violations: Up to 4% of global annual revenue or €20M
    - FDA violations: Product recalls, criminal penalties
    - SOX violations: Criminal penalties, executive liability
    - Export control violations: Up to $1M per violation, criminal charges
    """
}

CONTRACT_TYPES = [
    'Software_Licensing_Agreement', 'Cloud_Services_Agreement', 'Data_Processing_Agreement',
    'Professional_Services_Contract', 'Equipment_Lease', 'Supply_Agreement',
    'Distribution_Agreement', 'Partnership_Agreement', 'Consulting_Services_Agreement',
    'IT_Support_Contract', 'Marketing_Services_Agreement', 'Development_Agreement',
    'API_Integration_License', 'Subscription_Agreement', 'Service_Level_Agreement',
    'Construction_Contract', 'Equipment_Rental_Agreement', 'Vendor_Agreement',
    'Office_Lease_Agreement', 'Manufacturing_Agreement', 'Logistics_Contract',
    'Maintenance_Contract', 'Healthcare_Services_Agreement', 'Financial_Services_Agreement'
]

STATUSES = ['ACTIVE', 'EXPIRED', 'RENEWED', 'PENDING', 'WARNING']

PARTIES_A = [
    ('TechCorp Solutions', '123 Business Street, Tech City, TC 12345'),
    ('InnovateTech Inc', '456 Innovation Drive, Silicon Valley, SV 94000'),
    ('DataStream Systems', '789 Data Lane, Cloud City, CC 98765'),
    ('GlobalCorp Industries', '321 Enterprise Blvd, Corporate Park, CP 55555'),
    ('NexGen Technologies', '654 Future Avenue, Tech Hub, TH 77777'),
]

PARTIES_B = [
    ('BuildPro Construction', '456 Commerce Avenue, Business District, BD 67890'),
    ('DataVault Systems', '789 Security Boulevard, CyberCity, CY 54321'),
    ('CloudScale Networks', '321 Network Drive, Server Town, ST 11111'),
    ('SecureData Corp', '987 Privacy Lane, Encryption City, EC 22222'),
    ('VendorMax Solutions', '147 Supply Chain Road, Logistics Hub, LH 33333'),
]


def generate_contract_content(contract_num, status, risk_level, contract_type):
    """Generate complete contract content with appropriate risk factors."""
    
    profile = RISK_PROFILES[risk_level]
    
    # Generate values
    contract_value = random.randint(*profile['contract_value_range'])
    liability_cap = int(contract_value * random.uniform(*profile['liability_multiplier']))
    sla_penalty = random.randint(*profile['sla_penalty_range'])
    sla_percent = round((sla_penalty / contract_value) * 100, 1)
    termination_percent = random.randint(*profile['termination_fee_percent'])
    notice_days = random.randint(*profile['notice_days_range'])
    late_payment = random.randint(*profile['late_payment_percent'])
    cure_days = random.randint(*profile['cure_days'])
    cyber_insurance = random.randint(*profile['insurance']['cyber_range'])
    confidentiality_years = random.randint(*profile['confidentiality_years'])
    dispute_days = random.randint(*profile['dispute_days'])
    change_notice = random.randint(*profile['change_notice_days'])
    
    # Generate dates based on status
    start_date = datetime.now() - timedelta(days=random.randint(30, 365))
    if status == 'EXPIRED':
        end_date = datetime.now() - timedelta(days=random.randint(1, 180))
    elif status == 'WARNING':
        end_date = datetime.now() + timedelta(days=random.randint(1, 30))
    else:
        end_date = start_date + timedelta(days=random.randint(365, 1460))
    
    duration_days = (end_date - start_date).days
    
    # Select parties
    party_a = random.choice(PARTIES_A)
    party_b = random.choice(PARTIES_B)
    
    # SLA based on risk
    sla_types = {
        'LOW': 'Best effort, email support only',
        'MEDIUM': '99% uptime, business hours support, 24-hour response time',
        'HIGH': '99.9% uptime, business hours support, 4-hour response time',
        'CRITICAL': '99.99% uptime, 24/7 support, 1-hour response time, dedicated account manager'
    }
    
    contract_content = f"""
CONTRACT AGREEMENT
{contract_type.replace('_', ' ').upper()}

Contract Number: {contract_num}
Date of Agreement: {start_date.strftime('%B %d, %Y')}

PARTIES TO THE AGREEMENT:

Party A (The Company): {party_a[0]}
Address: {party_a[1]}
Email: contracts@{party_a[0].lower().replace(' ', '')}.com

Party B (The Vendor/Client): {party_b[0]}
Address: {party_b[1]}
Email: legal@{party_b[0].lower().replace(' ', '')}.com

WHEREAS, the parties wish to enter into this {contract_type.replace('_', ' ')} under the following terms and conditions:

1. SCOPE OF SERVICES
   {party_b[0]} shall provide {contract_type.replace('_', ' ').lower()} services to {party_a[0]} as detailed in Appendix A.
   This includes but is not limited to professional consultation, implementation, maintenance, and support services.

2. CONTRACT TERM
   Start Date: {start_date.strftime('%B %d, %Y')}
   End Date: {end_date.strftime('%B %d, %Y')}
   Contract Duration: {duration_days} days
   
   Status: {status}
   Risk Classification: {risk_level}

3. FINANCIAL TERMS
   Total Contract Value: ${contract_value:,} USD
   Payment Terms: {'Upon receipt' if risk_level == 'LOW' else 'Net 30 days' if risk_level == 'MEDIUM' else 'Quarterly, Net 30 days'}
   Currency: United States Dollars (USD)
   
   Payment Schedule:
   - Initial Payment: {random.randint(15, 40)}% upon contract signing
   - Milestone Payments: {random.randint(35, 55)}% upon completion of deliverables
   - Final Payment: {100 - random.randint(15, 40) - random.randint(35, 55)}% upon project acceptance

4. PAYMENT OBLIGATIONS
   All payments shall be made via wire transfer to the account specified by {party_b[0]}.
   Late payments will incur a penalty of {late_payment}% per month.
   Invoice disputes must be raised within {random.randint(10, 21)} business days.

5. SERVICE LEVEL AGREEMENT (SLA)
   {sla_types[risk_level]}
   
   Penalties for SLA Breaches:
   - Each breach: ${sla_penalty:,} or {sla_percent}% of monthly fees, whichever is greater
   - Repeated breaches may result in contract termination

6. KEY DATES AND MILESTONES
   - Contract Effective Date: {start_date.strftime('%B %d, %Y')}
   - First Milestone: {(start_date + timedelta(days=30)).strftime('%B %d, %Y')}
   - Mid-Point Review: {(start_date + timedelta(days=duration_days//2)).strftime('%B %d, %Y')}
   - Final Deliverable: {(end_date - timedelta(days=30)).strftime('%B %d, %Y')}
   - Contract Expiration: {end_date.strftime('%B %d, %Y')}

7. TERMINATION CLAUSES
   Either party may terminate this agreement under the following conditions:
   
   a) Termination for Convenience:
      - {notice_days} days written notice required
      - Termination fee: {termination_percent}% of remaining contract value
   
   b) Termination for Cause:
      - Immediate termination upon material breach
      - {cure_days} days to cure breach after written notice
      - No termination fee if other party is at fault
   
   c) Force Majeure:
      - Contract may be suspended during uncontrollable events
      - Extension of deadlines without penalties

8. LIABILITY AND INDEMNIFICATION
   Total Liability Cap: ${liability_cap:,} USD
   
   {party_b[0]} agrees to indemnify and hold harmless {party_a[0]} from:
   - Third-party claims arising from services provided
   - Intellectual property infringement claims
   - Data breaches or security incidents
   - Negligence or willful misconduct
   
   Exclusions:
   - Indirect, consequential, or punitive damages
   - Loss of profits or business opportunities
   - Claims arising from {party_a[0]}'s actions or instructions

9. INTELLECTUAL PROPERTY RIGHTS
   - All work product becomes property of {party_a[0]}
   - {party_b[0]} retains rights to pre-existing materials and tools
   - Limited license granted for use of proprietary methodologies
   - Confidentiality obligations survive contract termination

10. CONFIDENTIALITY
    Both parties agree to maintain confidentiality of:
    - Proprietary business information
    - Technical specifications and trade secrets
    - Financial information and pricing
    - Customer data and business strategies
    
    Confidentiality period: {confidentiality_years} years post-termination

11. INSURANCE REQUIREMENTS
    {party_b[0]} must maintain the following insurance:
    - General Liability: ${profile['insurance']['general']} minimum
    - Professional Liability: ${profile['insurance']['professional']} minimum
    - Cyber Liability: ${cyber_insurance:,} minimum
    - Workers Compensation: As required by law

{COMPLIANCE_DETAILS[risk_level]}

13. DISPUTE RESOLUTION
    - Initial negotiation period: {dispute_days} days
    - Mediation: If negotiation fails
    - Binding Arbitration: Final resolution method
    - Venue: {'Delaware' if risk_level in ['HIGH', 'CRITICAL'] else 'California'}

14. AMENDMENT AND MODIFICATION
    This contract may only be modified by written agreement signed by both parties.
    Change requests must be submitted in writing with {change_notice} days notice.

15. GOVERNING LAW
    This agreement shall be governed by the laws of the State of Delaware,
    without regard to its conflict of law provisions.

16. ENTIRE AGREEMENT
    This contract represents the entire agreement between the parties and supersedes
    all prior negotiations, representations, or agreements, whether written or oral.

SIGNATURES:

For {party_a[0]}:
_________________________________
Name: {random.choice(['Michael Chen', 'Sarah Johnson', 'David Martinez', 'Jennifer Smith'])}
Title: {random.choice(['VP of Operations', 'Director of Procurement', 'Chief Operating Officer'])}
Date: {start_date.strftime('%B %d, %Y')}

For {party_b[0]}:
_________________________________
Name: {random.choice(['Jennifer Brown', 'Robert Wilson', 'Maria Garcia', 'James Anderson'])}
Title: {random.choice(['VP of Sales', 'Director of Business Development', 'Chief Executive Officer'])}
Date: {start_date.strftime('%B %d, %Y')}

--- END OF CONTRACT ---

APPENDIX A: DETAILED SCOPE OF WORK
[Detailed technical specifications and deliverables would be listed here]

APPENDIX B: PRICING SCHEDULE
[Detailed breakdown of costs and payment milestones would be listed here]

APPENDIX C: SERVICE LEVEL AGREEMENT (SLA) METRICS
[Specific performance metrics and measurement criteria would be listed here]

Contract Status: {status}
Risk Level: {risk_level}
Generated for demo purposes with balanced risk assessment.
"""
    
    return contract_content


def update_existing_contracts():
    """Update existing 65 contracts with compliance factors."""
    demo_dir = Path('demo_contracts')
    contracts = sorted([f for f in demo_dir.iterdir() if f.suffix == '.txt' and f.name != 'README.md'])
    
    print(f"Updating {len(contracts)} existing contracts with compliance factors...")
    updated = 0
    
    for contract_file in contracts:
        # Parse filename
        parts = contract_file.stem.split('_')
        if len(parts) < 4:
            continue
            
        contract_num = parts[0]
        status = parts[1]
        risk_level = parts[2]
        contract_type = '_'.join(parts[3:])
        
        # Generate new content
        content = generate_contract_content(contract_num, status, risk_level, contract_type)
        
        # Write updated contract
        with open(contract_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] Updated {contract_file.name}")
        updated += 1
    
    print(f"\nUpdated {updated} existing contracts")
    return updated


def generate_new_contracts(start_num, count):
    """Generate new contracts with balanced distribution."""
    demo_dir = Path('demo_contracts')
    demo_dir.mkdir(exist_ok=True)
    
    # Calculate balanced distribution
    per_risk = count // 4
    per_status = count // 5
    
    # Create distribution plan
    risks = (['LOW'] * per_risk + ['MEDIUM'] * per_risk + 
             ['HIGH'] * per_risk + ['CRITICAL'] * (count - 3 * per_risk))
    random.shuffle(risks)
    
    statuses = (STATUSES * (count // 5 + 1))[:count]
    random.shuffle(statuses)
    
    print(f"\nGenerating {count} new contracts starting from CNT-2024-{start_num:04d}...")
    generated = 0
    
    for i in range(count):
        contract_num = f"CNT-2024-{start_num + i:04d}"
        status = statuses[i]
        risk_level = risks[i]
        contract_type = random.choice(CONTRACT_TYPES)
        
        filename = f"{contract_num}_{status}_{risk_level}_{contract_type}.txt"
        filepath = demo_dir / filename
        
        # Generate content
        content = generate_contract_content(contract_num, status, risk_level, contract_type)
        
        # Write contract
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] Generated {filename}")
        generated += 1
    
    print(f"\nGenerated {generated} new contracts")
    return generated


def print_distribution():
    """Print distribution of contracts."""
    demo_dir = Path('demo_contracts')
    contracts = [f for f in demo_dir.iterdir() if f.suffix == '.txt' and f.name != 'README.md']
    
    # Count by risk level
    risk_counts = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0, 'CRITICAL': 0}
    status_counts = {s: 0 for s in STATUSES}
    
    for contract in contracts:
        parts = contract.stem.split('_')
        if len(parts) >= 3:
            status = parts[1]
            risk_level = parts[2]
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1
            if status in status_counts:
                status_counts[status] += 1
    
    print("\n" + "="*60)
    print("FINAL DISTRIBUTION")
    print("="*60)
    print(f"\nTotal Contracts: {len(contracts)}")
    print("\nRisk Levels:")
    for risk, count in risk_counts.items():
        percentage = (count / len(contracts)) * 100
        print(f"  {risk:8s}: {count:3d} ({percentage:5.1f}%)")
    
    print("\nStatuses:")
    for status, count in status_counts.items():
        percentage = (count / len(contracts)) * 100
        print(f"  {status:8s}: {count:3d} ({percentage:5.1f}%)")
    print("="*60)


if __name__ == "__main__":
    print("="*60)
    print("Balanced Demo Contract Generator")
    print("="*60)
    print()
    
    # Update existing contracts
    existing_count = update_existing_contracts()
    
    # Generate 50 new contracts
    new_count = generate_new_contracts(start_num=66, count=50)
    
    # Print final distribution
    print_distribution()
    
    print("\nDone! All contracts updated with balanced risk assessment.")
    print("Upload contracts to verify AI assessments match risk levels!")
