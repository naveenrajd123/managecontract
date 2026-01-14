"""
Fix Demo Contract Risk Levels
Updates all demo contracts to match their filename risk level with appropriate content.
"""

import os
import re
import random
from pathlib import Path

# Risk profile templates
RISK_PROFILES = {
    'LOW': {
        'contract_value_range': (5000, 25000),
        'liability_multiplier': (2, 3),
        'sla_penalty_range': (100, 500),
        'termination_fee_percent': (5, 10),
        'notice_days_range': (30, 45),
        'late_payment_percent': (1, 2),
        'insurance': {
            'general_liability': '1M',
            'professional_liability': '500K',
            'cyber_liability_range': (100000, 250000)
        },
        'cure_days': (10, 15),
        'confidentiality_years': (1, 2),
        'dispute_negotiation_days': (10, 15),
        'change_notice_days': (14, 21)
    },
    'MEDIUM': {
        'contract_value_range': (25000, 100000),
        'liability_multiplier': (3, 4),
        'sla_penalty_range': (500, 2000),
        'termination_fee_percent': (10, 20),
        'notice_days_range': (45, 60),
        'late_payment_percent': (2, 3),
        'insurance': {
            'general_liability': '2M',
            'professional_liability': '1M',
            'cyber_liability_range': (250000, 500000)
        },
        'cure_days': (15, 20),
        'confidentiality_years': (2, 3),
        'dispute_negotiation_days': (15, 20),
        'change_notice_days': (21, 28)
    },
    'HIGH': {
        'contract_value_range': (100000, 500000),
        'liability_multiplier': (4, 5),
        'sla_penalty_range': (2000, 10000),
        'termination_fee_percent': (20, 30),
        'notice_days_range': (60, 90),
        'late_payment_percent': (3, 5),
        'insurance': {
            'general_liability': '5M',
            'professional_liability': '3M',
            'cyber_liability_range': (500000, 1000000)
        },
        'cure_days': (20, 30),
        'confidentiality_years': (3, 5),
        'dispute_negotiation_days': (20, 30),
        'change_notice_days': (28, 45)
    },
    'CRITICAL': {
        'contract_value_range': (500000, 2000000),
        'liability_multiplier': (5, 10),
        'sla_penalty_range': (10000, 50000),
        'termination_fee_percent': (30, 50),
        'notice_days_range': (90, 120),
        'late_payment_percent': (5, 8),
        'insurance': {
            'general_liability': '10M',
            'professional_liability': '5M',
            'cyber_liability_range': (1000000, 5000000)
        },
        'cure_days': (30, 45),
        'confidentiality_years': (5, 7),
        'dispute_negotiation_days': (30, 45),
        'change_notice_days': (45, 60)
    }
}


def parse_filename(filename):
    """Extract contract details from filename."""
    # Pattern: CNT-YYYY-NNNN_STATUS_RISKLEVEL_ContractType.txt
    pattern = r'(CNT-\d{4}-\d{4})_([A-Z]+)_([A-Z]+)_(.+)\.txt'
    match = re.match(pattern, filename)
    
    if match:
        return {
            'contract_number': match.group(1),
            'status': match.group(2),
            'risk_level': match.group(3),
            'contract_type': match.group(4).replace('_', ' ')
        }
    return None


def generate_risk_values(risk_level):
    """Generate appropriate values based on risk level."""
    profile = RISK_PROFILES.get(risk_level, RISK_PROFILES['LOW'])
    
    # Contract value
    contract_value = random.randint(*profile['contract_value_range'])
    
    # Liability cap
    liability_multiplier = random.uniform(*profile['liability_multiplier'])
    liability_cap = int(contract_value * liability_multiplier)
    
    # SLA penalty
    sla_penalty = random.randint(*profile['sla_penalty_range'])
    sla_percent = round((sla_penalty / contract_value) * 100, 1)
    
    # Termination fee
    termination_percent = random.randint(*profile['termination_fee_percent'])
    
    # Notice days
    notice_days = random.randint(*profile['notice_days_range'])
    
    # Late payment penalty
    late_payment_percent = random.randint(*profile['late_payment_percent'])
    
    # Cure days
    cure_days = random.randint(*profile['cure_days'])
    
    # Cyber liability
    cyber_liability = random.randint(*profile['insurance']['cyber_liability_range'])
    
    # Confidentiality
    confidentiality_years = random.randint(*profile['confidentiality_years'])
    
    # Dispute negotiation
    dispute_days = random.randint(*profile['dispute_negotiation_days'])
    
    # Change notice
    change_notice_days = random.randint(*profile['change_notice_days'])
    
    return {
        'contract_value': contract_value,
        'liability_cap': liability_cap,
        'sla_penalty': sla_penalty,
        'sla_percent': sla_percent,
        'termination_percent': termination_percent,
        'notice_days': notice_days,
        'late_payment_percent': late_payment_percent,
        'cure_days': cure_days,
        'general_liability': profile['insurance']['general_liability'],
        'professional_liability': profile['insurance']['professional_liability'],
        'cyber_liability': cyber_liability,
        'confidentiality_years': confidentiality_years,
        'dispute_days': dispute_days,
        'change_notice_days': change_notice_days
    }


def update_contract_content(content, risk_level, values):
    """Update contract content with risk-appropriate values."""
    
    # Update contract value
    content = re.sub(
        r'Total Contract Value: \$[\d,]+ USD',
        f'Total Contract Value: ${values["contract_value"]:,} USD',
        content
    )
    
    # Update late payment penalty
    content = re.sub(
        r'Late payments will incur a penalty of \d+% per month\.',
        f'Late payments will incur a penalty of {values["late_payment_percent"]}% per month.',
        content
    )
    
    # Update SLA penalty
    content = re.sub(
        r'Each breach: \$[\d,]+ or \d+% of monthly fees',
        f'Each breach: ${values["sla_penalty"]:,} or {values["sla_percent"]}% of monthly fees',
        content
    )
    
    # Update termination notice period
    content = re.sub(
        r'\d+ days written notice required',
        f'{values["notice_days"]} days written notice required',
        content
    )
    
    # Update termination fee
    content = re.sub(
        r'Termination fee: \d+% of remaining contract value',
        f'Termination fee: {values["termination_percent"]}% of remaining contract value',
        content
    )
    
    # Update cure period
    content = re.sub(
        r'\d+ days to cure breach',
        f'{values["cure_days"]} days to cure breach',
        content
    )
    
    # Update liability cap
    content = re.sub(
        r'Total Liability Cap: \$[\d,]+ USD',
        f'Total Liability Cap: ${values["liability_cap"]:,} USD',
        content
    )
    
    # Update insurance requirements
    content = re.sub(
        r'General Liability: \$\d+M minimum',
        f'General Liability: ${values["general_liability"]} minimum',
        content
    )
    content = re.sub(
        r'Professional Liability: \$\d+[KM] minimum',
        f'Professional Liability: ${values["professional_liability"]} minimum',
        content
    )
    content = re.sub(
        r'Cyber Liability: \$[\d,]+ minimum',
        f'Cyber Liability: ${values["cyber_liability"]:,} minimum',
        content
    )
    
    # Update confidentiality period
    content = re.sub(
        r'Confidentiality period: \d+ years post-termination',
        f'Confidentiality period: {values["confidentiality_years"]} years post-termination',
        content
    )
    
    # Update dispute resolution negotiation period
    content = re.sub(
        r'Initial negotiation period: \d+ days',
        f'Initial negotiation period: {values["dispute_days"]} days',
        content
    )
    
    # Update change request notice
    content = re.sub(
        r'Change requests must be submitted in writing with \d+ days notice\.',
        f'Change requests must be submitted in writing with {values["change_notice_days"]} days notice.',
        content
    )
    
    # Update risk classification in contract body
    content = re.sub(
        r'Risk Classification: [A-Z]+',
        f'Risk Classification: {risk_level}',
        content
    )
    
    # Update risk level at end
    content = re.sub(
        r'Risk Level: [A-Z]+',
        f'Risk Level: {risk_level}',
        content
    )
    
    return content


def process_contracts(demo_contracts_dir):
    """Process all contracts in the demo_contracts directory."""
    contracts_dir = Path(demo_contracts_dir)
    
    if not contracts_dir.exists():
        print(f"Error: Directory {demo_contracts_dir} not found!")
        return
    
    # Get all .txt files
    contract_files = sorted([f for f in contracts_dir.iterdir() if f.suffix == '.txt'])
    
    print(f"Found {len(contract_files)} contract files to process...")
    print()
    
    updated_count = 0
    skipped_count = 0
    
    for contract_file in contract_files:
        # Parse filename
        file_info = parse_filename(contract_file.name)
        
        if not file_info:
            print(f"[SKIP] {contract_file.name} - invalid filename format")
            skipped_count += 1
            continue
        
        risk_level = file_info['risk_level']
        
        if risk_level not in RISK_PROFILES:
            print(f"[SKIP] {contract_file.name} - unknown risk level: {risk_level}")
            skipped_count += 1
            continue
        
        # Read contract
        try:
            with open(contract_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[ERROR] Reading {contract_file.name}: {e}")
            skipped_count += 1
            continue
        
        # Generate risk-appropriate values
        values = generate_risk_values(risk_level)
        
        # Update content
        updated_content = update_contract_content(content, risk_level, values)
        
        # Write back
        try:
            with open(contract_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"[OK] Updated {contract_file.name} ({risk_level} risk)")
            updated_count += 1
        except Exception as e:
            print(f"[ERROR] Writing {contract_file.name}: {e}")
            skipped_count += 1
    
    print()
    print("=" * 60)
    print(f"Successfully updated: {updated_count} contracts")
    if skipped_count > 0:
        print(f"Skipped: {skipped_count} contracts")
    print("=" * 60)


if __name__ == "__main__":
    # Run from project root
    demo_contracts_dir = "demo_contracts"
    
    print("=" * 60)
    print("Demo Contract Risk Level Fix Script")
    print("=" * 60)
    print()
    
    process_contracts(demo_contracts_dir)
    
    print()
    print("Done! All contracts have been updated.")
    print("Upload some contracts to verify the AI assessments are correct.")
