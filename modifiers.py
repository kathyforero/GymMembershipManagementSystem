"""
Price modifiers for the Gym Membership Management System.
Uses Strategy Pattern with abstract base class and Chain of Responsibility.
"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple, List


class PriceModifier(ABC):
    """Abstract base class for price modifiers (discounts/surcharges)."""
    
    @abstractmethod
    def apply(self, context: Dict) -> Tuple[int, str]:
        """Apply modification to price. Returns (amount, message)."""
        pass
    
    @abstractmethod
    def can_apply(self, context: Dict) -> bool:
        """Check if this modifier can be applied."""
        pass


class PremiumSurchargeModifier(PriceModifier):
    """Applies 15% surcharge for premium features."""
    
    def can_apply(self, context: Dict) -> bool:
        return context.get('has_premium_features', False)
    
    def apply(self, context: Dict) -> Tuple[int, str]:
        subtotal = context.get('subtotal', 0)
        surcharge = int(subtotal * 0.15)
        return surcharge, f"Premium features surcharge (15%): +${surcharge}"


class GroupDiscountModifier(PriceModifier):
    """Applies 10% discount for groups of 2+."""
    
    def can_apply(self, context: Dict) -> bool:
        return context.get('group_size', 1) >= 2
    
    def apply(self, context: Dict) -> Tuple[int, str]:
        cost = context.get('subtotal_with_surcharge', context.get('subtotal', 0))
        group_size = context.get('group_size', 1)
        discount = int(cost * 0.10)
        return discount, f"Group discount (10% for {group_size}): -${discount}"


class SpecialOfferModifier(PriceModifier):
    """Applies special offer discounts based on total cost."""
    
    def can_apply(self, context: Dict) -> bool:
        cost = context.get('subtotal_with_surcharge', context.get('subtotal', 0))
        return cost > 200
    
    def apply(self, context: Dict) -> Tuple[int, str]:
        cost = context.get('subtotal_with_surcharge', context.get('subtotal', 0))
        if cost > 400:
            return 50, "Special offer (>$400): -$50"
        elif cost > 200:
            return 20, "Special offer (>$200): -$20"
        return 0, ""


class PriceModifierChain:
    """Chain of Responsibility for applying price modifiers."""
    
    def __init__(self, modifiers: List[PriceModifier]):
        self.modifiers = modifiers
    
    def apply_all(self, context: Dict) -> Dict:
        """Apply all applicable modifiers and return results."""
        results = {
            'premium_surcharge': 0,
            'premium_msg': '',
            'group_discount': 0,
            'group_msg': '',
            'special_discount': 0,
            'special_msg': ''
        }
        
        for modifier in self.modifiers:
            if modifier.can_apply(context):
                amount, msg = modifier.apply(context)
                
                if isinstance(modifier, PremiumSurchargeModifier):
                    results['premium_surcharge'] = amount
                    results['premium_msg'] = msg
                    context['subtotal_with_surcharge'] = (
                        context.get('subtotal', 0) + amount
                    )
                elif isinstance(modifier, GroupDiscountModifier):
                    results['group_discount'] = amount
                    results['group_msg'] = msg
                elif isinstance(modifier, SpecialOfferModifier):
                    results['special_discount'] = amount
                    results['special_msg'] = msg
        
        return results

