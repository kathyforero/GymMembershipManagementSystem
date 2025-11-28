"""Quick test to verify imports work correctly."""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gym_membership import GymMembershipSystem
    from models import MembershipPlan, AdditionalFeature, FeatureType
    print("✓ All imports successful")
    
    # Quick functionality test
    system = GymMembershipSystem()
    result = system.calculate_total_cost("premium", ["personal_training"], 1)
    assert result["valid"] is True
    assert result["total"] > 0
    print("✓ System functionality verified")
    print("\n✅ All checks passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

