#!/usr/bin/env python3
"""
Regenerate demo contracts with realistic risk distribution:
- 20% LOW (23 contracts)
- 30% MEDIUM (35 contracts)  
- 40% HIGH (46 contracts)
- 10% CRITICAL (12 contracts)
Total: 116 contracts
"""

import os
import random
from datetime import datetime, timedelta

# Risk distribution (out of 116 total)
RISK_DISTRIBUTION = {
    'LOW': 23,      # 20%
    'MEDIUM': 35,   # 30%
    'HIGH': 46,     # 40%
    'CRITICAL': 12  # 10%
}

# Status distribution (similar to before)
STATUS_OPTIONS = ['ACTIVE', 'EXPIRED', 'RENEWED', 'PENDING', 'WARNING']
STATUS_WEIGHTS = [0.25, 0.15, 0.15, 0.15, 0.30]  # WARNING is most common for demo

# Contract types
CONTRACT_TYPES = [
    'Software Licensing Agreement',
    'Cloud Services Agreement',
    'Data Processing Agreement',
    'Service Level Agreement',
    'Consulting Services Agreement',
    'Equipment Lease',
    'Office Lease Agreement',
    'Distribution Agreement',
    'Partnership Agreement',
    'Vendor Agreement',
    'Supply Agreement',
    'Professional Services Contract',
    'API Integration License',
    'Development Agreement',
    'Marketing Services Agreement',
    'IT Support Contract',
    'Subscription Agreement',
    'Construction Contract',
    'Equipment Rental Agreement',
    'Logistics Contract',
    'Manufacturing Agreement',
    'Maintenance Contract',
    'Healthcare Services Agreement',
    'Financial Services Agreement'
]

# Party names
PARTY_A_NAMES = [
    'TechCorp Solutions',
    'InnovateTech Inc',
    'GlobalCorp Industries',
    'Enterprise Systems LLC',
    'Digital Dynamics Corp'
]

PARTY_B_NAMES = [
    'DataVault Systems',
    'CloudScale Networks',
    'SecureData Inc',
    'VendorMax Solutions',
    'BuildPro Construction'
]


def get_risk_profile(risk_level):
    """Return financial and compliance parameters for each risk level"""
    
    if risk_level == 'LOW':
        return {
            'value_range': (5000, 24999),
            'sla_penalty_range': (100, 499),
            'termination_fee_pct': random.randint(3, 9),
            'liability_multiplier': random.uniform(2.0, 3.0),
            'notice_days': random.randint(20, 45),
            'cure_days': random.randint(7, 15),
            'confidentiality_years': random.randint(1, 2),
            'uptime': 'Best effort, email support only',
            'insurance_general': '1M',
            'insurance_professional': '500K',
            'compliance': [
                'All applicable federal, state, and local laws',
                'General business regulations',
                'Standard data protection practices',
                'Anti-corruption and ethics policies'
            ],
            'compliance_note': ''
        }
    
    elif risk_level == 'MEDIUM':
        return {
            'value_range': (25000, 99999),
            'sla_penalty_range': (500, 1999),
            'termination_fee_pct': random.randint(10, 20),
            'liability_multiplier': random.uniform(3.0, 4.0),
            'notice_days': random.randint(40, 70),
            'cure_days': random.randint(15, 25),
            'confidentiality_years': random.randint(3, 5),
            'uptime': '99.5% uptime, business hours support, 8-hour response time',
            'insurance_general': '3M',
            'insurance_professional': '2M',
            'compliance': [
                'All applicable federal, state, and local laws',
                'GDPR (General Data Protection Regulation) - Personal data handling',
                'CCPA (California Consumer Privacy Act)',
                'SOC 2 Type II certification recommended',
                'ISO 27001 Information Security Management',
                'State privacy laws compliance',
                'Anti-corruption and ethics policies (FCPA, UK Bribery Act)'
            ],
            'compliance_note': '''
    Standard Compliance Requirements:
    - Annual third-party security assessment recommended
    - Data Processing Agreements (DPA) required
    - Breach notification within 72 hours
    - Right to audit upon 30 days notice
    - Standard encryption requirements
    '''
        }
    
    elif risk_level == 'HIGH':
        return {
            'value_range': (100000, 499999),
            'sla_penalty_range': (2000, 9999),
            'termination_fee_pct': random.randint(20, 30),
            'liability_multiplier': random.uniform(4.0, 5.0),
            'notice_days': random.randint(60, 90),
            'cure_days': random.randint(20, 35),
            'confidentiality_years': random.randint(5, 7),
            'uptime': '99.9% uptime, business hours support, 4-hour response time',
            'insurance_general': '5M',
            'insurance_professional': '3M',
            'compliance': [
                'All applicable federal, state, and local laws',
                'GDPR (General Data Protection Regulation) - Full compliance required',
                'PCI-DSS Level 1 - Payment card data security standards',
                'SOC 2 Type II certification - Annual audit required',
                'ISO 27001 Information Security Management',
                'Privacy Shield Framework (if applicable)',
                'State privacy laws (CCPA, CPRA, etc.)',
                'Anti-corruption and ethics policies (FCPA, UK Bribery Act)'
            ],
            'compliance_note': '''
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
    '''
        }
    
    else:  # CRITICAL
        return {
            'value_range': (500000, 2000000),
            'sla_penalty_range': (10000, 50000),
            'termination_fee_pct': random.randint(35, 50),
            'liability_multiplier': random.uniform(5.0, 8.0),
            'notice_days': random.randint(90, 120),
            'cure_days': random.randint(30, 45),
            'confidentiality_years': random.randint(7, 10),
            'uptime': '99.99% uptime, 24/7 support, 1-hour response time, dedicated account manager',
            'insurance_general': '10M',
            'insurance_professional': '5M',
            'compliance': [
                'All applicable federal, state, and local laws',
                'HIPAA (Health Insurance Portability and Accountability Act)',
                'Protected Health Information (PHI) handling requirements',
                'HITECH Act - Security and breach notification',
                'GDPR with extensive personal data processing',
                'FDA regulations for medical devices/software',
                'SOX (Sarbanes-Oxley) financial reporting requirements',
                'PCI-DSS Level 1 - Payment card industry standards',
                'Export control regulations (ITAR, EAR)',
                'Critical infrastructure protection (NERC CIP, FISMA)',
                'State privacy laws (CCPA, CPRA, HIPAA state laws)',
                'FedRAMP compliance (if government contract)',
                'ISO 27001, ISO 13485 (medical devices)',
                'Anti-corruption (FCPA, UK Bribery Act, local laws)'
            ],
            'compliance_note': '''
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
    '''
        }


def generate_contract(contract_num, status, risk_level, contract_type):
    """Generate a single contract with realistic terms"""
    
    profile = get_risk_profile(risk_level)
    
    # Generate financial terms
    contract_value = random.randint(*profile['value_range'])
    sla_penalty = random.randint(*profile['sla_penalty_range'])
    liability_cap = int(contract_value * profile['liability_multiplier'])
    cyber_insurance = int(contract_value * random.uniform(1.5, 2.5))
    
    # Generate dates
    start_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 365))
    duration_days = random.randint(300, 1200)
    end_date = start_date + timedelta(days=duration_days)
    
    # Select parties
    party_a = random.choice(PARTY_A_NAMES)
    party_b = random.choice(PARTY_B_NAMES)
    
    # Payment terms
    payment_initial = random.randint(20, 40)
    payment_milestone = random.randint(35, 50)
    payment_final = 100 - payment_initial - payment_milestone
    
    # Generate contract content
    contract = f"""
CONTRACT AGREEMENT
{contract_type.upper()}

Contract Number: CNT-2024-{contract_num:04d}
Date of Agreement: {start_date.strftime('%B %d, %Y')}

PARTIES TO THE AGREEMENT:

Party A (The Company): {party_a}
Address: 123 Business Street, Tech City, TC 12345
Email: contracts@{party_a.lower().replace(' ', '')}.com

Party B (The Vendor/Client): {party_b}
Address: 789 Security Boulevard, CyberCity, CY 54321
Email: legal@{party_b.lower().replace(' ', '')}.com

WHEREAS, the parties wish to enter into this {contract_type} under the following terms and conditions:

1. SCOPE OF SERVICES
   {party_b} shall provide {contract_type.lower()} services to {party_a} as detailed in Appendix A.
   This includes but is not limited to professional consultation, implementation, maintenance, and support services.

2. CONTRACT TERM
   Start Date: {start_date.strftime('%B %d, %Y')}
   End Date: {end_date.strftime('%B %d, %Y')}
   Contract Duration: {duration_days} days
   
   Status: {status}
   Risk Classification: {risk_level}

3. FINANCIAL TERMS
   Total Contract Value: ${contract_value:,} USD
   Payment Terms: {'Upon receipt' if contract_value < 25000 else 'Quarterly, Net 30 days'}
   Currency: United States Dollars (USD)
   
   Payment Schedule:
   - Initial Payment: {payment_initial}% upon contract signing
   - Milestone Payments: {payment_milestone}% upon completion of deliverables
   - Final Payment: {payment_final}% upon project acceptance

4. PAYMENT OBLIGATIONS
   All payments shall be made via wire transfer to the account specified by {party_b}.
   Late payments will incur a penalty of {random.randint(1, 6)}% per month.
   Invoice disputes must be raised within {random.randint(10, 20)} business days.

5. SERVICE LEVEL AGREEMENT (SLA)
   {profile['uptime']}
   
   Penalties for SLA Breaches:
   - Each breach: ${sla_penalty:,} or {random.uniform(1.5, 6.5):.1f}% of monthly fees, whichever is greater
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
      - {profile['notice_days']} days written notice required
      - Termination fee: {profile['termination_fee_pct']}% of remaining contract value
   
   b) Termination for Cause:
      - Immediate termination upon material breach
      - {profile['cure_days']} days to cure breach after written notice
      - No termination fee if other party is at fault
   
   c) Force Majeure:
      - Contract may be suspended during uncontrollable events
      - Extension of deadlines without penalties

8. LIABILITY AND INDEMNIFICATION
   Total Liability Cap: ${liability_cap:,} USD
   
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
    
    Confidentiality period: {profile['confidentiality_years']} years post-termination

11. INSURANCE REQUIREMENTS
    {party_b} must maintain the following insurance:
    - General Liability: ${profile['insurance_general']} minimum
    - Professional Liability: ${profile['insurance_professional']} minimum
    - Cyber Liability: ${cyber_insurance:,} minimum
    - Workers Compensation: As required by law


12. COMPLIANCE AND REGULATORY
    Both parties shall comply with:"""
    
    for compliance_item in profile['compliance']:
        contract += f"\n    - {compliance_item}"
    
    if profile['compliance_note']:
        contract += f"\n    {profile['compliance_note']}"
    
    contract += f"""

13. DISPUTE RESOLUTION
    - Initial negotiation period: {random.randint(10, 40)} days
    - Mediation: If negotiation fails
    - Binding Arbitration: Final resolution method
    - Venue: {random.choice(['Delaware', 'California', 'New York'])}

14. AMENDMENT AND MODIFICATION
    This contract may only be modified by written agreement signed by both parties.
    Change requests must be submitted in writing with {random.randint(15, 50)} days notice.

15. GOVERNING LAW
    This agreement shall be governed by the laws of the State of Delaware,
    without regard to its conflict of law provisions.

16. ENTIRE AGREEMENT
    This contract represents the entire agreement between the parties and supersedes
    all prior negotiations, representations, or agreements, whether written or oral.

SIGNATURES:

For {party_a}:
_________________________________
Name: {random.choice(['Michael Chen', 'Sarah Johnson', 'David Martinez', 'Jennifer Smith', 'Robert Taylor'])}
Title: {random.choice(['Director of Procurement', 'Chief Operating Officer', 'VP of Operations', 'General Counsel'])}
Date: {start_date.strftime('%B %d, %Y')}

For {party_b}:
_________________________________
Name: {random.choice(['Emily Davis', 'James Anderson', 'Maria Garcia', 'John Wilson', 'Jennifer Brown'])}
Title: {random.choice(['Chief Executive Officer', 'VP of Sales', 'Director of Business Development', 'President'])}
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
Generated for demo purposes with realistic risk distribution (20% LOW, 30% MEDIUM, 40% HIGH, 10% CRITICAL).
"""
    
    return contract


def main():
    """Generate all contracts with realistic distribution"""
    
    output_dir = 'demo_contracts'
    os.makedirs(output_dir, exist_ok=True)
    
    # Build list of contracts to generate
    contracts_to_generate = []
    contract_num = 1
    
    for risk_level, count in RISK_DISTRIBUTION.items():
        for _ in range(count):
            status = random.choices(STATUS_OPTIONS, weights=STATUS_WEIGHTS)[0]
            contract_type = random.choice(CONTRACT_TYPES)
            contracts_to_generate.append((contract_num, status, risk_level, contract_type))
            contract_num += 1
    
    # Shuffle to randomize order
    random.shuffle(contracts_to_generate)
    
    # Generate each contract
    print(f"Generating {len(contracts_to_generate)} contracts with realistic distribution...")
    print(f"  LOW: {RISK_DISTRIBUTION['LOW']} (20%)")
    print(f"  MEDIUM: {RISK_DISTRIBUTION['MEDIUM']} (30%)")
    print(f"  HIGH: {RISK_DISTRIBUTION['HIGH']} (40%)")
    print(f"  CRITICAL: {RISK_DISTRIBUTION['CRITICAL']} (10%)")
    print()
    
    for i, (num, status, risk, ctype) in enumerate(contracts_to_generate, 1):
        filename = f"CNT-2024-{num:04d}_{status}_{risk}_{ctype.replace(' ', '_')}.txt"
        filepath = os.path.join(output_dir, filename)
        
        contract_content = generate_contract(num, status, risk, ctype)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(contract_content)
        
        print(f"[{i}/116] Generated: {filename}")
    
    print(f"\n[SUCCESS] Generated 116 contracts in {output_dir}/")
    print("\nDistribution:")
    print(f"  LOW: {RISK_DISTRIBUTION['LOW']} contracts (20%)")
    print(f"  MEDIUM: {RISK_DISTRIBUTION['MEDIUM']} contracts (30%)")
    print(f"  HIGH: {RISK_DISTRIBUTION['HIGH']} contracts (40%)")
    print(f"  CRITICAL: {RISK_DISTRIBUTION['CRITICAL']} contracts (10%)")


if __name__ == '__main__':
    main()
