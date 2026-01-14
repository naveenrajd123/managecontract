"""
Add More Contracts with Balanced Distribution
This script adds contracts to reach a target total while maintaining balanced distribution.
"""

import asyncio
import sys
from pathlib import Path
import random
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.database import Contract, Base
from src.config import settings


# Contract templates for realistic data
PARTIES_A = ["TechCorp Solutions", "Global Dynamics Inc", "Acme Corporation", "MegaSoft Ltd"]
PARTIES_B = [
    "DataVault Systems", "CloudNet Services", "SecureHost Inc", "FastShip Logistics",
    "BuildPro Construction", "MediaMax Agency", "LegalEase LLC", "FinanceFirst Bank",
    "HealthTech Medical", "EduSmart Academy", "RetailGiant Corp", "AutoParts Warehouse",
    "FoodService Distributors", "GreenEnergy Solutions", "TravelHub International",
    "InsureTech Group", "PropertyPro Realty", "ManuFact Industries", "ConsultPro Services"
]

CONTRACT_TYPES = [
    "Software Licensing Agreement", "Service Level Agreement", "Equipment Lease",
    "Consulting Services Agreement", "Maintenance Contract", "Subscription Agreement",
    "Partnership Agreement", "Distribution Agreement", "Supply Agreement",
    "Cloud Services Agreement", "Professional Services Contract", "Marketing Services Agreement",
    "IT Support Contract", "Office Lease Agreement", "Equipment Rental Agreement",
    "Development Agreement", "API Integration License", "Data Processing Agreement",
    "Vendor Agreement", "Construction Contract"
]


def generate_contract_data(index, risk_level, status):
    """Generate realistic contract data."""
    now = datetime.now()
    
    contract_type = random.choice(CONTRACT_TYPES)
    party_a = random.choice(PARTIES_A)
    party_b = random.choice(PARTIES_B)
    
    # Generate contract number
    contract_number = f"CNT-2024-{1000 + index:03d}"
    
    # Set contract value based on risk level
    if risk_level == 'critical':
        value = random.uniform(500000, 2000000)
    elif risk_level == 'high':
        value = random.uniform(100000, 500000)
    elif risk_level == 'medium':
        value = random.uniform(25000, 100000)
    else:  # low
        value = random.uniform(5000, 25000)
    
    # Set dates based on status
    if status == 'expired':
        end_date = now - timedelta(days=random.randint(1, 90))
        start_date = end_date - timedelta(days=random.randint(365, 1095))
    elif status == 'warning':
        end_date = now + timedelta(days=random.randint(10, 60))
        start_date = now - timedelta(days=random.randint(180, 730))
    elif status == 'pending':
        start_date = now + timedelta(days=random.randint(1, 60))
        end_date = start_date + timedelta(days=random.randint(365, 1095))
    elif status == 'renewed':
        start_date = now - timedelta(days=random.randint(1, 90))
        end_date = now + timedelta(days=random.randint(730, 1825))
    else:  # active
        start_date = now - timedelta(days=random.randint(90, 730))
        end_date = now + timedelta(days=random.randint(180, 1095))
    
    # Risk reasons
    risk_reasons = {
        'low': f'Low-value {contract_type.lower()} with standard terms and minimal business impact',
        'medium': f'Standard {contract_type.lower()} with moderate value and typical commercial terms',
        'high': f'High-value {contract_type.lower()} requiring active monitoring and compliance oversight',
        'critical': f'Mission-critical {contract_type.lower()} with significant financial exposure and complex obligations'
    }
    
    # Summaries
    summary = f"This is a {contract_type.lower()} between {party_a} and {party_b}. "
    if risk_level in ['high', 'critical']:
        summary += "The contract includes stringent SLAs, penalty clauses, and requires ongoing compliance monitoring. "
    summary += f"The agreement has a total value of ${value:,.2f} and covers a period of {(end_date - start_date).days} days."
    
    return {
        'contract_name': contract_type,
        'contract_number': contract_number,
        'party_a': party_a,
        'party_b': party_b,
        'start_date': start_date,
        'end_date': end_date,
        'status': status,
        'contract_value': value,
        'currency': 'USD',
        'risk_level': risk_level,
        'risk_reason': risk_reasons[risk_level],
        'summary': summary,
        'file_type': 'txt',
        'created_at': now,
        'updated_at': now
    }


async def add_contracts(target_total=55):
    """Add contracts to reach target total."""
    
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Get current count
        result = await session.execute(select(func.count(Contract.id)))
        current_total = result.scalar()
        
        contracts_to_add = target_total - current_total
        
        if contracts_to_add <= 0:
            print(f"Already have {current_total} contracts. No need to add more.")
            return
        
        print(f"\nCurrent contracts: {current_total}")
        print(f"Target total: {target_total}")
        print(f"Contracts to add: {contracts_to_add}\n")
        
        # Target percentages (same as before)
        risk_distribution = {
            'low': 0.30,
            'medium': 0.35,
            'high': 0.25,
            'critical': 0.10
        }
        
        status_distribution = {
            'active': 0.50,
            'pending': 0.20,
            'warning': 0.15,
            'renewed': 0.10,
            'expired': 0.05
        }
        
        # Calculate how many of each to add
        risk_assignments = []
        for risk, pct in risk_distribution.items():
            count = int(contracts_to_add * pct)
            risk_assignments.extend([risk] * count)
        
        status_assignments = []
        for status, pct in status_distribution.items():
            count = int(contracts_to_add * pct)
            status_assignments.extend([status] * count)
        
        # Adjust for rounding
        while len(risk_assignments) < contracts_to_add:
            risk_assignments.append('medium')
        while len(status_assignments) < contracts_to_add:
            status_assignments.append('active')
        
        # Shuffle for randomness
        random.shuffle(risk_assignments)
        random.shuffle(status_assignments)
        
        print("Adding contracts...")
        
        # Get max existing contract number
        result = await session.execute(
            select(func.max(Contract.id))
        )
        max_id = result.scalar() or 0
        
        # Add contracts
        for i in range(contracts_to_add):
            risk = risk_assignments[i]
            status = status_assignments[i]
            
            contract_data = generate_contract_data(max_id + i + 1, risk, status)
            contract = Contract(**contract_data)
            session.add(contract)
            
            if (i + 1) % 10 == 0:
                print(f"  Added {i + 1}/{contracts_to_add} contracts...")
        
        await session.commit()
        print(f"\n[OK] Successfully added {contracts_to_add} contracts!\n")
        
        # Show final distribution
        print("="*60)
        print("FINAL DISTRIBUTION")
        print("="*60)
        
        result = await session.execute(select(func.count(Contract.id)))
        total = result.scalar()
        print(f"\nTotal Contracts: {total}")
        
        print("\nRisk Level Distribution:")
        for risk in ['low', 'medium', 'high', 'critical']:
            result = await session.execute(
                select(func.count(Contract.id)).where(Contract.risk_level == risk)
            )
            count = result.scalar()
            print(f"  {risk.capitalize():10s}: {count:3d} ({count/total*100:.1f}%)")
        
        print("\nStatus Distribution:")
        for status in ['active', 'expired', 'renewed', 'pending', 'warning']:
            result = await session.execute(
                select(func.count(Contract.id)).where(Contract.status == status)
            )
            count = result.scalar()
            print(f"  {status.capitalize():10s}: {count:3d} ({count/total*100:.1f}%)")
        
        print("="*60 + "\n")
    
    await engine.dispose()


if __name__ == "__main__":
    print("="*60)
    print("ADD BALANCED CONTRACTS")
    print("="*60)
    print("\nThis will add contracts to reach ~55 total")
    print("while maintaining balanced distribution.\n")
    
    asyncio.run(add_contracts(target_total=55))
    print("[SUCCESS] Contract addition complete!")
