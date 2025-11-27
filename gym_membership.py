"""
Gym Membership Management System - Main Application
Uses modular architecture with separated responsibilities.
"""

from typing import Dict, List, Optional, Tuple
from models import MembershipPlan, AdditionalFeature, FeatureType
from validators import MembershipValidator, FeatureListValidator, FeatureValidator
from modifiers import (
    PremiumSurchargeModifier,
    GroupDiscountModifier,
    SpecialOfferModifier,
    PriceModifierChain
)
from factories import MembershipFactory, FeatureFactory
from display import MembershipDisplay, FeatureDisplay, SummaryDisplay


class GymMembershipSystem:
    """Main system orchestrating all components."""
    
    def __init__(self):
        self.membership_plans = MembershipFactory.create_all()
        self.features = FeatureFactory.create_all()
        self.membership_validator = MembershipValidator()
        self.feature_validator = FeatureValidator()
        self.feature_list_validator = FeatureListValidator(self.feature_validator)
        
        # Chain of modifiers
        self.modifier_chain = PriceModifierChain([
            PremiumSurchargeModifier(),
            GroupDiscountModifier(),
            SpecialOfferModifier()
        ])
        
        # Display components
        self.membership_display = MembershipDisplay()
        self.feature_display = FeatureDisplay()
        self.summary_display = SummaryDisplay()
    
    def validate_membership(self, key: str) -> Tuple[bool, Optional[str]]:
        """Validate membership selection."""
        return self.membership_validator.validate(key, self.membership_plans)
    
    def validate_features(self, keys: List[str]) -> Tuple[bool, Optional[str], List[str]]:
        """Validate feature selections."""
        return self.feature_list_validator.validate(keys, self.features)
    
    def _calculate_base_costs(
        self, membership_key: str, feature_keys: List[str]
    ) -> Tuple[int, int, bool]:
        """Calculate base costs and check for premium features."""
        plan = self.membership_plans[membership_key.lower()]
        base_cost = plan.cost
        features_cost = sum(self.features[f].cost for f in feature_keys)
        has_premium = any(
            self.features[f].feature_type == FeatureType.PREMIUM
            for f in feature_keys
        )
        return base_cost, features_cost, has_premium
    
    def calculate_total_cost(
        self, membership_key: str, feature_keys: List[str], group_size: int = 1
    ) -> Dict:
        """Calculate total cost with all modifiers."""
        # Validate
        is_valid, error = self.validate_membership(membership_key)
        if not is_valid:
            return {"valid": False, "error": error, "total": -1}
        
        is_valid, error, valid_features = self.validate_features(feature_keys)
        if not is_valid:
            return {"valid": False, "error": error, "total": -1}
        
        # Calculate base costs
        base_cost, features_cost, has_premium = self._calculate_base_costs(
            membership_key, valid_features
        )
        subtotal = base_cost + features_cost
        
        # Build context for modifiers
        context = {
            'subtotal': subtotal,
            'group_size': group_size,
            'has_premium_features': has_premium
        }
        
        # Apply modifiers
        modifier_results = self.modifier_chain.apply_all(context)
        
        # Calculate final total
        total = (
            subtotal +
            modifier_results['premium_surcharge'] -
            modifier_results['group_discount'] -
            modifier_results['special_discount']
        )
        
        plan = self.membership_plans[membership_key.lower()]
        return {
            "valid": True,
            "base_cost": base_cost,
            "features_cost": features_cost,
            "subtotal": subtotal,
            "premium_surcharge": modifier_results['premium_surcharge'],
            "premium_msg": modifier_results['premium_msg'],
            "group_discount": modifier_results['group_discount'],
            "group_msg": modifier_results['group_msg'],
            "special_discount": modifier_results['special_discount'],
            "special_msg": modifier_results['special_msg'],
            "total": max(0, total),
            "membership_name": plan.name,
            "selected_features": [self.features[f].name for f in valid_features]
        }
    
    def display_membership_plans(self) -> None:
        """Display membership plans."""
        self.membership_display.display(self.membership_plans)
    
    def display_additional_features(self) -> None:
        """Display additional features."""
        self.feature_display.display(self.features)
    
    def display_summary(self, result: Dict) -> None:
        """Display summary."""
        self.summary_display.display(result)
    
    def process_membership(
        self, membership_key: str, feature_keys: List[str],
        group_size: int = 1, confirmed: bool = False
    ) -> int:
        """Process membership and return total cost or -1."""
        if not confirmed:
            return -1
        
        result = self.calculate_total_cost(membership_key, feature_keys, group_size)
        return result["total"] if result["valid"] else -1
    
    # Compatibility methods for tests
    @property
    def additional_features(self) -> Dict[str, AdditionalFeature]:
        """Compatibility property for tests."""
        return self.features
    
    def validate_membership_selection(self, membership_key: str) -> Tuple[bool, Optional[str]]:
        """Compatibility method for tests."""
        return self.validate_membership(membership_key)
    
    def validate_feature_selection(self, feature_keys: List[str]) -> Tuple[bool, Optional[str], List[str]]:
        """Compatibility method for tests."""
        return self.validate_features(feature_keys)
    
    def calculate_base_cost(self, membership_key: str) -> int:
        """Compatibility method for tests."""
        return self.membership_plans[membership_key.lower()].cost
    
    def calculate_features_cost(self, feature_keys: List[str]) -> int:
        """Compatibility method for tests."""
        return sum(self.features[f.lower()].cost for f in feature_keys)
    
    def has_premium_features(self, feature_keys: List[str]) -> bool:
        """Compatibility method for tests."""
        return any(
            self.features[f.lower()].feature_type == FeatureType.PREMIUM
            for f in feature_keys
        )
    
    def calculate_group_discount(self, total_cost: int, group_size: int) -> Tuple[int, str]:
        """Compatibility method for tests."""
        modifier = GroupDiscountModifier()
        context = {'subtotal_with_surcharge': total_cost, 'group_size': group_size}
        if modifier.can_apply(context):
            return modifier.apply(context)
        return 0, ""
    
    def calculate_special_offer_discount(self, total_cost: int) -> Tuple[int, str]:
        """Compatibility method for tests."""
        modifier = SpecialOfferModifier()
        context = {'subtotal_with_surcharge': total_cost}
        if modifier.can_apply(context):
            return modifier.apply(context)
        return 0, ""
    
    def calculate_premium_surcharge(self, total_cost: int, has_premium: bool) -> Tuple[int, str]:
        """Compatibility method for tests."""
        modifier = PremiumSurchargeModifier()
        context = {'subtotal': total_cost, 'has_premium_features': has_premium}
        if modifier.can_apply(context):
            return modifier.apply(context)
        return 0, ""


# ============================================================================
# User Interface Functions
# ============================================================================

def get_user_input(prompt: str, valid_options: Optional[List[str]] = None) -> str:
    """Get validated user input."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Please enter a value.")
            continue
        if valid_options and value.lower() not in [o.lower() for o in valid_options]:
            print(f"Invalid. Choose: {', '.join(valid_options)}")
            continue
        return value


def get_integer_input(prompt: str, min_value: int = 1) -> int:
    """Get integer input."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value < min_value:
                print(f"Enter value >= {min_value}")
                continue
            return value
        except ValueError:
            print("Enter a valid integer.")


def main():
    """Main application entry point."""
    system = GymMembershipSystem()
    
    print("\n" + "="*60)
    print("WELCOME TO THE GYM MEMBERSHIP MANAGEMENT SYSTEM")
    print("="*60)
    
    system.display_membership_plans()
    
    membership_key = get_user_input(
        "\nSelect membership (basic/premium/family): ",
        ["basic", "premium", "family"]
    ).lower()
    
    system.display_additional_features()
    
    features_input = input(
        "\nEnter feature keys (comma-separated) or Enter for none: "
    ).strip()
    feature_keys = [f.strip().lower() for f in features_input.split(",")] if features_input else []
    
    group_size = get_integer_input("\nGroup size (min 1): ", min_value=1)
    
    if group_size >= 2:
        print(f"\n💡 10% group discount for {group_size} members!")
    
    result = system.calculate_total_cost(membership_key, feature_keys, group_size)
    system.display_summary(result)
    
    if not result["valid"]:
        print("Processing canceled due to errors.")
        return -1
    
    confirm = get_user_input("Confirm? (yes/no): ", ["yes", "no"]).lower()
    
    if confirm == "yes":
        total = system.process_membership(membership_key, feature_keys, group_size, True)
        print(f"\n✅ Membership confirmed! Total: ${total}")
        return total
    else:
        print("\n❌ Canceled.")
        return -1


if __name__ == "__main__":
    main()
