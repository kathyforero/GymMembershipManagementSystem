"""
Display components for the Gym Membership Management System.
Uses Strategy Pattern with abstract base class.
"""

from abc import ABC, abstractmethod
from typing import Dict
from models import FeatureType


class DisplayComponent(ABC):
    """Abstract base class for display components."""
    
    @abstractmethod
    def display(self, items: Dict) -> None:
        """Display items."""
        pass


class MembershipDisplay(DisplayComponent):
    """Displays membership plans."""
    
    def display(self, items: Dict) -> None:
        print("\n" + "="*60)
        print("AVAILABLE MEMBERSHIP PLANS")
        print("="*60)
        for key, plan in items.items():
            status = "✓ Available" if plan.available else "✗ Unavailable"
            print(f"\n{plan.name} - ${plan.cost}/month [{status}]")
            print("Benefits:")
            for benefit in plan.benefits:
                print(f"  • {benefit}")
        print("\n" + "="*60)


class FeatureDisplay(DisplayComponent):
    """Displays additional features."""
    
    def display(self, items: Dict) -> None:
        print("\n" + "="*60)
        print("ADDITIONAL FEATURES")
        print("="*60)
        
        standard = [
            (k, v) for k, v in items.items()
            if v.feature_type == FeatureType.STANDARD
        ]
        premium = [
            (k, v) for k, v in items.items()
            if v.feature_type == FeatureType.PREMIUM
        ]
        
        if standard:
            print("\nStandard Features:")
            for key, feature in standard:
                status = "✓" if feature.available else "✗"
                print(f"  [{key}] {feature.name} - ${feature.cost} [{status}]")
        
        if premium:
            print("\nPremium Features (15% surcharge):")
            for key, feature in premium:
                status = "✓" if feature.available else "✗"
                print(f"  [{key}] {feature.name} - ${feature.cost} [{status}]")
        
        print("\n" + "="*60)


class SummaryDisplay(DisplayComponent):
    """Displays membership summary."""
    
    def display(self, result: Dict) -> None:
        if not result.get("valid", False):
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
            return
        
        print("\n" + "="*60)
        print("MEMBERSHIP SUMMARY")
        print("="*60)
        print(f"\nMembership: {result['membership_name']}")
        print(f"Base Cost: ${result['base_cost']}")
        
        if result['selected_features']:
            print("\nFeatures:")
            for feature in result['selected_features']:
                print(f"  • {feature}")
            print(f"Features Cost: ${result['features_cost']}")
        
        print(f"\nSubtotal: ${result['subtotal']}")
        
        for msg_key in ['premium_msg', 'group_msg', 'special_msg']:
            msg = result.get(msg_key, "")
            if msg:
                print(msg)
        
        print(f"\n{'='*60}")
        print(f"TOTAL: ${result['total']}")
        print(f"{'='*60}\n")

