"""
Validators for the Gym Membership Management System.
Uses Strategy Pattern with abstract base class.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple


class Validator(ABC):
    """Abstract base class for validators."""
    
    @abstractmethod
    def validate(self, value: str, registry: Dict) -> Tuple[bool, Optional[str]]:
        """Validate a value against a registry."""
        pass


class MembershipValidator(Validator):
    """Validates membership selection."""
    
    def validate(self, value: str, registry: Dict) -> Tuple[bool, Optional[str]]:
        key = value.lower()
        if key not in registry:
            options = ', '.join(registry.keys())
            return False, f"Invalid membership: {value}. Choose: {options}"
        
        plan = registry[key]
        if not plan.available:
            return False, f"Membership '{plan.name}' is unavailable."
        
        return True, None


class FeatureValidator(Validator):
    """Validates feature selection."""
    
    def validate(self, value: str, registry: Dict) -> Tuple[bool, Optional[str]]:
        key = value.lower()
        if key not in registry:
            return False, f"Invalid feature: {value}."
        
        feature = registry[key]
        if not feature.available:
            return False, f"Feature '{feature.name}' is unavailable."
        
        return True, None


class FeatureListValidator:
    """Validates a list of features."""
    
    def __init__(self, feature_validator: FeatureValidator):
        self.feature_validator = feature_validator
    
    def validate(self, feature_keys: List[str], registry: Dict) -> Tuple[bool, Optional[str], List[str]]:
        """Validate multiple features and return valid keys."""
        valid_keys = []
        for key in feature_keys:
            is_valid, error = self.feature_validator.validate(key, registry)
            if not is_valid:
                return False, error, []
            valid_keys.append(key.lower())
        return True, None, valid_keys


