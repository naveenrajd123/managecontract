"""
Rebalance Contract Database
This script rebalances contracts to have a realistic distribution across:
- Risk Levels: low, medium, high, critical
- Status: active, expired, renewed, pending, warning
"""

import asyncio
import sys
from pathlib import Path
import random
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.database import Contract, Base
from src.config import settings


async def get_current_distribution(session: AsyncSession):
    """Get current distribution of contracts."""
    print("\n" + "="*60)
    print("CURRENT DISTRIBUTION")
    print("="*60)
    
    # Total contracts
    result = await session.execute(select(func.count(Contract.id)))
    total = result.scalar()
    print(f"\nTotal Contracts: {total}")
    
    # Risk level distribution
    print("\nRisk Level Distribution:")
    for risk in ['low', 'medium', 'high', 'critical']:
        result = await session.execute(
            select(func.count(Contract.id)).where(Contract.risk_level == risk)
        )
        count = result.scalar()
        print(f"  {risk.capitalize():10s}: {count:3d} ({count/total*100:.1f}%)")
    
    # Status distribution
    print("\nStatus Distribution:")
    for status in ['active', 'expired', 'renewed', 'pending', 'warning']:
        result = await session.execute(
            select(func.count(Contract.id)).where(Contract.status == status)
        )
        count = result.scalar()
        print(f"  {status.capitalize():10s}: {count:3d} ({count/total*100:.1f}%)")
    
    print("="*60 + "\n")


async def rebalance_contracts():
    """Rebalance contracts in the database."""
    
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Show current distribution
        await get_current_distribution(session)
        
        # Get all contracts
        result = await session.execute(select(Contract))
        all_contracts = result.scalars().all()
        
        print(f"Loaded {len(all_contracts)} contracts for rebalancing...\n")
        
        # Separate critical contracts from others
        critical_contracts = [c for c in all_contracts if c.risk_level == 'critical']
        other_contracts = [c for c in all_contracts if c.risk_level != 'critical']
        
        print(f"Found {len(critical_contracts)} critical contracts")
        print(f"Found {len(other_contracts)} non-critical contracts\n")
        
        # Delete 35 critical contracts (keep 15)
        contracts_to_delete = random.sample(critical_contracts, min(35, len(critical_contracts)))
        print(f"Deleting {len(contracts_to_delete)} critical contracts...")
        
        for contract in contracts_to_delete:
            await session.delete(contract)
        
        await session.commit()
        print("[OK] Deleted critical contracts\n")
        
        # Get remaining contracts
        result = await session.execute(select(Contract))
        remaining_contracts = result.scalars().all()
        
        total_remaining = len(remaining_contracts)
        print(f"Remaining contracts: {total_remaining}")
        
        # Define target distribution (balanced)
        # Risk levels: roughly equal distribution
        target_risk_distribution = {
            'low': int(total_remaining * 0.30),      # 30%
            'medium': int(total_remaining * 0.35),   # 35%
            'high': int(total_remaining * 0.25),     # 25%
            'critical': total_remaining - int(total_remaining * 0.90)  # 10%
        }
        
        # Status: realistic distribution
        target_status_distribution = {
            'active': int(total_remaining * 0.50),    # 50%
            'pending': int(total_remaining * 0.20),   # 20%
            'warning': int(total_remaining * 0.15),   # 15%
            'renewed': int(total_remaining * 0.10),   # 10%
            'expired': total_remaining - int(total_remaining * 0.95)  # 5%
        }
        
        print("\nTarget Distribution:")
        print("Risk Levels:")
        for risk, count in target_risk_distribution.items():
            print(f"  {risk.capitalize():10s}: {count:3d} ({count/total_remaining*100:.1f}%)")
        
        print("\nStatus:")
        for status, count in target_status_distribution.items():
            print(f"  {status.capitalize():10s}: {count:3d} ({count/total_remaining*100:.1f}%)")
        
        # Shuffle contracts for random assignment
        random.shuffle(remaining_contracts)
        
        print("\nReassigning risk levels and statuses...")
        
        # Assign risk levels
        risk_assignments = []
        for risk, count in target_risk_distribution.items():
            risk_assignments.extend([risk] * count)
        
        # Adjust if total doesn't match (rounding issues)
        while len(risk_assignments) < total_remaining:
            risk_assignments.append('medium')
        while len(risk_assignments) > total_remaining:
            risk_assignments.pop()
        
        random.shuffle(risk_assignments)
        
        # Assign statuses
        status_assignments = []
        for status, count in target_status_distribution.items():
            status_assignments.extend([status] * count)
        
        # Adjust if total doesn't match
        while len(status_assignments) < total_remaining:
            status_assignments.append('active')
        while len(status_assignments) > total_remaining:
            status_assignments.pop()
        
        random.shuffle(status_assignments)
        
        # Apply assignments
        for i, contract in enumerate(remaining_contracts):
            contract.risk_level = risk_assignments[i]
            contract.status = status_assignments[i]
            
            # Update risk_reason based on new risk level
            risk_reasons = {
                'low': 'Low financial impact and standard terms',
                'medium': 'Moderate value contract with standard risk factors',
                'high': 'High value contract requiring careful monitoring',
                'critical': 'Critical contract with significant business impact and complex terms'
            }
            contract.risk_reason = risk_reasons.get(contract.risk_level, 'Standard risk assessment')
            
            # Adjust dates based on status
            now = datetime.now()
            
            if contract.status == 'expired':
                # Set end date in the past
                contract.end_date = now - timedelta(days=random.randint(1, 90))
                contract.start_date = contract.end_date - timedelta(days=random.randint(365, 1095))
            
            elif contract.status == 'warning':
                # Set end date within 30-60 days
                contract.end_date = now + timedelta(days=random.randint(10, 60))
                contract.start_date = now - timedelta(days=random.randint(180, 730))
            
            elif contract.status == 'pending':
                # Set start date in the future
                contract.start_date = now + timedelta(days=random.randint(1, 60))
                contract.end_date = contract.start_date + timedelta(days=random.randint(365, 1095))
            
            elif contract.status == 'renewed':
                # Recent start date, far end date
                contract.start_date = now - timedelta(days=random.randint(1, 90))
                contract.end_date = now + timedelta(days=random.randint(730, 1825))
            
            else:  # active
                # Normal active contract
                contract.start_date = now - timedelta(days=random.randint(90, 730))
                contract.end_date = now + timedelta(days=random.randint(180, 1095))
            
            contract.updated_at = datetime.now()
        
        await session.commit()
        print("[OK] Updated all contract risk levels and statuses\n")
        
        # Show new distribution
        await get_current_distribution(session)
        
        print("[SUCCESS] Rebalancing complete!")
        print("\nYour dashboard should now show a balanced distribution across")
        print("all risk levels and statuses for a more realistic view.\n")
    
    await engine.dispose()


if __name__ == "__main__":
    print("="*60)
    print("CONTRACT DATABASE REBALANCING TOOL")
    print("="*60)
    print("\nThis script will:")
    print("1. Remove ~35 critical contracts")
    print("2. Rebalance remaining contracts across risk levels")
    print("3. Assign realistic statuses (active, pending, warning, etc.)")
    print("\n[!] This will modify your database!")
    print("="*60 + "\n")
    
    response = input("Continue? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        print("\n>>> Starting rebalancing...\n")
        asyncio.run(rebalance_contracts())
    else:
        print("\n[X] Rebalancing cancelled.")
