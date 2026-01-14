"""
Early Warning System
Monitors contracts and generates alerts for important dates and risks.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Contract
from src.config import settings


class EarlyWarningSystem:
    """
    Monitors contracts and generates warnings for:
    - Upcoming expirations
    - Renewal deadlines
    - Compliance dates
    - High-risk contracts
    """
    
    def __init__(self):
        """Initialize the warning system with configured thresholds."""
        self.critical_days = settings.WARNING_DAYS_CRITICAL
        self.warning_days = settings.WARNING_DAYS_WARNING
        self.info_days = settings.WARNING_DAYS_INFO
    
    async def get_all_warnings(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Get all active warnings across all contracts.
        
        Returns:
            List of warning dictionaries with details
        """
        warnings = []
        
        # Get all active contracts
        result = await db.execute(
            select(Contract).where(Contract.status == "active")
        )
        contracts = result.scalars().all()
        
        current_date = datetime.utcnow()
        
        for contract in contracts:
            # Check for expiration warnings
            days_until_expiry = (contract.end_date - current_date).days
            
            if days_until_expiry <= self.critical_days and days_until_expiry > 0:
                warnings.append({
                    "contract_id": contract.id,
                    "contract_name": contract.contract_name,
                    "contract_number": contract.contract_number,
                    "warning_type": "expiration",
                    "severity": "critical",
                    "days_remaining": days_until_expiry,
                    "message": f"Contract expires in {days_until_expiry} days!",
                    "due_date": contract.end_date.isoformat()
                })
            elif days_until_expiry <= self.warning_days and days_until_expiry > self.critical_days:
                warnings.append({
                    "contract_id": contract.id,
                    "contract_name": contract.contract_name,
                    "contract_number": contract.contract_number,
                    "warning_type": "expiration",
                    "severity": "warning",
                    "days_remaining": days_until_expiry,
                    "message": f"Contract expires in {days_until_expiry} days",
                    "due_date": contract.end_date.isoformat()
                })
            elif days_until_expiry <= self.info_days and days_until_expiry > self.warning_days:
                warnings.append({
                    "contract_id": contract.id,
                    "contract_name": contract.contract_name,
                    "contract_number": contract.contract_number,
                    "warning_type": "expiration",
                    "severity": "info",
                    "days_remaining": days_until_expiry,
                    "message": f"Contract expires in {days_until_expiry} days",
                    "due_date": contract.end_date.isoformat()
                })
            
            # Check for expired contracts that haven't been updated
            if days_until_expiry < 0:
                warnings.append({
                    "contract_id": contract.id,
                    "contract_name": contract.contract_name,
                    "contract_number": contract.contract_number,
                    "warning_type": "expired",
                    "severity": "critical",
                    "days_remaining": days_until_expiry,
                    "message": f"Contract expired {abs(days_until_expiry)} days ago!",
                    "due_date": contract.end_date.isoformat()
                })
            
            # Check for high-risk contracts
            if contract.risk_level in ["high", "critical"]:
                warnings.append({
                    "contract_id": contract.id,
                    "contract_name": contract.contract_name,
                    "contract_number": contract.contract_number,
                    "warning_type": "high_risk",
                    "severity": contract.risk_level,
                    "message": f"Contract marked as {contract.risk_level} risk",
                    "risk_level": contract.risk_level
                })
        
        # Sort warnings by severity
        severity_order = {"critical": 0, "high": 1, "warning": 2, "medium": 3, "info": 4, "low": 5}
        warnings.sort(key=lambda x: severity_order.get(x["severity"], 999))
        
        return warnings
    
    async def get_contract_warnings(
        self,
        db: AsyncSession,
        contract_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get warnings for a specific contract.
        
        Args:
            db: Database session
            contract_id: Contract ID to check
        
        Returns:
            List of warnings for this contract
        """
        result = await db.execute(
            select(Contract).where(Contract.id == contract_id)
        )
        contract = result.scalar_one_or_none()
        
        if not contract:
            return []
        
        warnings = []
        current_date = datetime.utcnow()
        days_until_expiry = (contract.end_date - current_date).days
        
        # Expiration check
        if days_until_expiry <= self.critical_days and days_until_expiry > 0:
            warnings.append({
                "warning_type": "expiration",
                "severity": "critical",
                "days_remaining": days_until_expiry,
                "message": f"Contract expires in {days_until_expiry} days!"
            })
        elif days_until_expiry < 0:
            warnings.append({
                "warning_type": "expired",
                "severity": "critical",
                "message": f"Contract expired {abs(days_until_expiry)} days ago!"
            })
        
        # Risk check
        if contract.risk_level in ["high", "critical"]:
            warnings.append({
                "warning_type": "high_risk",
                "severity": contract.risk_level,
                "message": f"Contract has {contract.risk_level} risk level"
            })
        
        return warnings
    
    def get_dashboard_stats(self, warnings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics for dashboard display.
        
        Args:
            warnings: List of all warnings
        
        Returns:
            Statistics dictionary
        """
        stats = {
            "total_warnings": len(warnings),
            "critical_count": 0,
            "warning_count": 0,
            "info_count": 0,
            "expired_count": 0,
            "high_risk_count": 0,
        }
        
        for warning in warnings:
            severity = warning.get("severity", "")
            warning_type = warning.get("warning_type", "")
            
            if severity == "critical":
                stats["critical_count"] += 1
            elif severity in ["warning", "high"]:
                stats["warning_count"] += 1
            elif severity == "info":
                stats["info_count"] += 1
            
            if warning_type == "expired":
                stats["expired_count"] += 1
            elif warning_type == "high_risk":
                stats["high_risk_count"] += 1
        
        return stats


# Create global instance
early_warning_system = EarlyWarningSystem()
