"""Patient entity."""

from dataclasses import dataclass, field
from datetime import date
from typing import Any
from uuid import UUID

from domain.exceptions import InvalidCPFError


def validate_cpf(cpf: str) -> bool:
    """Validate Brazilian CPF.
    
    Args:
        cpf: CPF string (with or without formatting)
        
    Returns:
        True if valid, False otherwise
    """
    # Remove non-numeric characters
    cpf = "".join(filter(str.isdigit, cpf))
    
    # Check length
    if len(cpf) != 11:
        return False
    
    # Check if all digits are the same
    if len(set(cpf)) == 1:
        return False
    
    # Validate first digit
    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit1 = (sum1 * 10) % 11
    digit1 = 0 if digit1 == 10 else digit1
    
    if digit1 != int(cpf[9]):
        return False
    
    # Validate second digit
    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit2 = (sum2 * 10) % 11
    digit2 = 0 if digit2 == 10 else digit2
    
    return digit2 == int(cpf[10])


def format_cpf(cpf: str) -> str:
    """Format CPF as XXX.XXX.XXX-XX.
    
    Args:
        cpf: Raw CPF string
        
    Returns:
        Formatted CPF
    """
    digits = "".join(filter(str.isdigit, cpf))
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:11]}"


@dataclass
class Patient:
    """Patient aggregate root."""
    
    user_id: UUID
    full_name: str
    cpf: str
    email: str
    birth_date: date
    gender: str
    id: int | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: dict[str, Any] | None = None
    medical_history: dict[str, Any] = field(default_factory=dict)
    allergies: list[str] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Validate entity after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate patient data."""
        if not self.full_name or len(self.full_name.strip()) < 3:
            raise InvalidCPFError("Full name must have at least 3 characters")
        
        if not validate_cpf(self.cpf):
            raise InvalidCPFError(f"Invalid CPF: {self.cpf}")
        
        self.cpf = format_cpf(self.cpf)
        
        if self.gender not in ("male", "female", "other", "prefer_not_to_say"):
            raise InvalidCPFError(
                "Gender must be: male, female, other, or prefer_not_to_say"
            )
    
    def update_medical_history(self, data: dict[str, Any]) -> None:
        """Update medical history."""
        self.medical_history.update(data)
    
    def add_allergy(self, allergy: str) -> None:
        """Add allergy if not already present."""
        if allergy not in self.allergies:
            self.allergies.append(allergy)
    
    def remove_allergy(self, allergy: str) -> None:
        """Remove allergy if present."""
        if allergy in self.allergies:
            self.allergies.remove(allergy)
    
    def update_emergency_contact(self, contact: dict[str, Any]) -> None:
        """Update emergency contact."""
        self.emergency_contact = contact
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "user_id": str(self.user_id),
            "full_name": self.full_name,
            "cpf": self.cpf,
            "email": self.email,
            "phone": self.phone,
            "birth_date": self.birth_date.isoformat(),
            "gender": self.gender,
            "address": self.address,
            "emergency_contact": self.emergency_contact,
            "medical_history": self.medical_history,
            "allergies": self.allergies,
        }
