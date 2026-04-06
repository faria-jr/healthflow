"""Doctor entity."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any
from uuid import UUID

from domain.exceptions import InvalidCRMError


def validate_crm(crm: str) -> bool:
    """Validate Brazilian CRM.
    
    Format: CRM/UF 123456 or CRM123456UF
    
    Args:
        crm: CRM string
        
    Returns:
        True if valid, False otherwise
    """
    import re
    
    # Remove extra spaces
    crm = crm.strip().upper()
    
    # Pattern: CRM/UF 123456 or CRM123456UF
    pattern = r"^CRM[/]?([A-Z]{2})\s*(\d{4,6})$|^CRM(\d{4,6})([A-Z]{2})$"
    match = re.match(pattern, crm)
    
    if not match:
        return False
    
    # Valid Brazilian states
    valid_states = {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
        "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
        "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
    }
    
    # Extract state from match
    state = match.group(1) or match.group(4)
    return state in valid_states


def format_crm(crm: str) -> str:
    """Format CRM as CRM/UF XXXXXX.
    
    Args:
        crm: Raw CRM string
        
    Returns:
        Formatted CRM
    """
    import re
    
    crm = crm.strip().upper()
    
    # Try to extract state and number
    pattern = r"CRM[/]?([A-Z]{2})\s*(\d+)|CRM(\d+)([A-Z]{2})"
    match = re.search(pattern, crm)
    
    if match:
        if match.group(1):  # CRM/UF format
            state = match.group(1)
            number = match.group(2)
        else:  # CRM123UF format
            number = match.group(3)
            state = match.group(4)
        return f"CRM/{state} {number}"
    
    return crm


@dataclass
class Doctor:
    """Doctor aggregate root."""
    
    user_id: UUID
    full_name: str
    crm: str
    specialty: str
    email: str
    id: int | None = None
    phone: str | None = None
    bio: str | None = None
    consultation_fee: Decimal | None = None
    is_active: bool = True
    
    def __post_init__(self) -> None:
        """Validate entity after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate doctor data."""
        if not self.full_name or len(self.full_name.strip()) < 3:
            raise InvalidCRMError("Full name must have at least 3 characters")
        
        if not validate_crm(self.crm):
            raise InvalidCRMError(f"Invalid CRM: {self.crm}")
        
        self.crm = format_crm(self.crm)
        
        if not self.specialty or len(self.specialty.strip()) < 2:
            raise InvalidCRMError("Specialty must have at least 2 characters")
        
        if self.consultation_fee is not None and self.consultation_fee < 0:
            raise InvalidCRMError("Consultation fee cannot be negative")
    
    def deactivate(self) -> None:
        """Deactivate doctor."""
        self.is_active = False
    
    def activate(self) -> None:
        """Activate doctor."""
        self.is_active = True
    
    def update_bio(self, bio: str) -> None:
        """Update bio."""
        self.bio = bio
    
    def update_fee(self, fee: Decimal) -> None:
        """Update consultation fee."""
        if fee < 0:
            raise InvalidCRMError("Consultation fee cannot be negative")
        self.consultation_fee = fee
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "user_id": str(self.user_id),
            "full_name": self.full_name,
            "crm": self.crm,
            "specialty": self.specialty,
            "phone": self.phone,
            "email": self.email,
            "bio": self.bio,
            "consultation_fee": str(self.consultation_fee) if self.consultation_fee else None,
            "is_active": self.is_active,
        }
