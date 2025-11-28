"""
Gym Membership Management System Package
"""

# Optional imports - only import if modules are available
# This allows the package to work even if modules aren't in the path
try:
    from gym_membership import GymMembershipSystem
    from models import MembershipPlan, AdditionalFeature, FeatureType
    
    __all__ = [
        'GymMembershipSystem',
        'MembershipPlan',
        'AdditionalFeature',
        'FeatureType'
    ]
except ImportError:
    # If imports fail, define empty __all__ to prevent errors
    __all__ = []


