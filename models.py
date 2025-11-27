"""
Data models for the Gym Membership Management System.
"""

from dataclasses import dataclass
from typing import List
from enum import Enum


class FeatureType(Enum):
    """Enumeration of feature types."""
    STANDARD = "standard"
    PREMIUM = "premium"


@dataclass
class MembershipPlan:
    """Represents a membership plan."""
    name: str
    cost: int
    benefits: List[str]
    available: bool = True
    
    def __str__(self):
        return f"{self.name} - ${self.cost}/month"


@dataclass
class AdditionalFeature:
    """Represents an additional feature."""
    name: str
    cost: int
    feature_type: FeatureType
    available: bool = True
    
    def __str__(self):
        return f"{self.name} - ${self.cost}"

