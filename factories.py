"""
Factories for creating membership plans and features.
Uses Factory Pattern.
"""

from typing import Dict
from models import MembershipPlan, AdditionalFeature, FeatureType


class MembershipFactory:
    """Factory for creating membership plans."""
    
    @staticmethod
    def create_all() -> Dict[str, MembershipPlan]:
        """Create all available membership plans."""
        return {
            "basic": MembershipPlan(
                name="Basic",
                cost=50,
                benefits=[
                    "Access to gym facilities",
                    "Locker room access",
                    "Basic equipment usage"
                ]
            ),
            "premium": MembershipPlan(
                name="Premium",
                cost=100,
                benefits=[
                    "All Basic benefits",
                    "Access to premium equipment",
                    "Priority booking",
                    "Nutrition consultation"
                ]
            ),
            "family": MembershipPlan(
                name="Family",
                cost=150,
                benefits=[
                    "All Premium benefits",
                    "Up to 4 family members",
                    "Family fitness classes",
                    "Childcare services"
                ]
            )
        }


class FeatureFactory:
    """Factory for creating additional features."""
    
    @staticmethod
    def create_all() -> Dict[str, AdditionalFeature]:
        """Create all available features."""
        return {
            "personal_training": AdditionalFeature(
                "Personal Training Sessions", 60, FeatureType.STANDARD
            ),
            "group_classes": AdditionalFeature(
                "Group Classes", 30, FeatureType.STANDARD
            ),
            "exclusive_facilities": AdditionalFeature(
                "Exclusive Facilities Access", 80, FeatureType.PREMIUM
            ),
            "specialized_training": AdditionalFeature(
                "Specialized Training Programs", 100, FeatureType.PREMIUM
            ),
            "nutrition_plan": AdditionalFeature(
                "Custom Nutrition Plan", 40, FeatureType.STANDARD
            ),
            "spa_access": AdditionalFeature(
                "Spa and Wellness Access", 70, FeatureType.PREMIUM
            )
        }

