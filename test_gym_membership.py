"""
Unit tests for the Gym Membership Management System.
Using pytest framework.
"""

import pytest
from gym_membership import GymMembershipSystem
from models import MembershipPlan, AdditionalFeature, FeatureType


class TestMembershipPlan:
    """Test cases for MembershipPlan class."""
    
    def test_membership_plan_creation(self):
        """Test creating a membership plan."""
        plan = MembershipPlan("Basic", 50, ["Access to gym"], True)
        assert plan.name == "Basic"
        assert plan.cost == 50
        assert len(plan.benefits) == 1
        assert plan.available is True
    
    def test_membership_plan_str(self):
        """Test string representation of membership plan."""
        plan = MembershipPlan("Premium", 100, ["Benefits"], True)
        assert "Premium" in str(plan)
        assert "100" in str(plan)


class TestAdditionalFeature:
    """Test cases for AdditionalFeature class."""
    
    def test_feature_creation(self):
        """Test creating an additional feature."""
        feature = AdditionalFeature("Personal Training", 60, FeatureType.STANDARD, True)
        assert feature.name == "Personal Training"
        assert feature.cost == 60
        assert feature.feature_type == FeatureType.STANDARD
        assert feature.available is True


@pytest.fixture
def system():
    """Fixture to create a GymMembershipSystem instance."""
    return GymMembershipSystem()


class TestGymMembershipSystem:
    """Test cases for GymMembershipSystem class."""
    
    def test_initialization(self, system):
        """Test system initialization."""
        assert system.membership_plans is not None
        assert system.additional_features is not None
        assert "basic" in system.membership_plans
        assert "premium" in system.membership_plans
        assert "family" in system.membership_plans
    
    def test_validate_membership_selection_valid(self, system):
        """Test validation of valid membership selection."""
        is_valid, error = system.validate_membership_selection("basic")
        assert is_valid is True
        assert error is None
    
    def test_validate_membership_selection_invalid_key(self, system):
        """Test validation of invalid membership key."""
        is_valid, error = system.validate_membership_selection("invalid")
        assert is_valid is False
        assert error is not None
    
    def test_validate_membership_selection_unavailable(self, system):
        """Test validation of unavailable membership."""
        # Make a plan unavailable
        system.membership_plans["basic"].available = False
        is_valid, error = system.validate_membership_selection("basic")
        assert is_valid is False
        assert error is not None
        # Restore for other tests
        system.membership_plans["basic"].available = True
    
    def test_validate_feature_selection_valid(self, system):
        """Test validation of valid feature selection."""
        is_valid, error, features = system.validate_feature_selection(["personal_training"])
        assert is_valid is True
        assert error is None
        assert len(features) == 1
    
    def test_validate_feature_selection_invalid_key(self, system):
        """Test validation of invalid feature key."""
        is_valid, error, features = system.validate_feature_selection(["invalid_feature"])
        assert is_valid is False
        assert error is not None
        assert len(features) == 0
    
    def test_validate_feature_selection_unavailable(self, system):
        """Test validation of unavailable feature."""
        # Make a feature unavailable
        system.additional_features["personal_training"].available = False
        is_valid, error, features = system.validate_feature_selection(["personal_training"])
        assert is_valid is False
        assert error is not None
        # Restore for other tests
        system.additional_features["personal_training"].available = True
    
    def test_validate_feature_selection_multiple(self, system):
        """Test validation of multiple features."""
        is_valid, error, features = system.validate_feature_selection(
            ["personal_training", "group_classes"]
        )
        assert is_valid is True
        assert len(features) == 2
    
    def test_calculate_base_cost(self, system):
        """Test base cost calculation."""
        cost = system.calculate_base_cost("basic")
        assert cost == 50
        
        cost = system.calculate_base_cost("premium")
        assert cost == 100
        
        cost = system.calculate_base_cost("family")
        assert cost == 150
    
    def test_calculate_features_cost_single(self, system):
        """Test feature cost calculation for single feature."""
        cost = system.calculate_features_cost(["personal_training"])
        assert cost == 60
    
    def test_calculate_features_cost_multiple(self, system):
        """Test feature cost calculation for multiple features."""
        cost = system.calculate_features_cost(["personal_training", "group_classes"])
        assert cost == 90  # 60 + 30
    
    def test_calculate_features_cost_empty(self, system):
        """Test feature cost calculation for no features."""
        cost = system.calculate_features_cost([])
        assert cost == 0
    
    def test_has_premium_features_true(self, system):
        """Test premium feature detection when premium features are present."""
        has_premium = system.has_premium_features(["exclusive_facilities"])
        assert has_premium is True
    
    def test_has_premium_features_false(self, system):
        """Test premium feature detection when no premium features are present."""
        has_premium = system.has_premium_features(["personal_training", "group_classes"])
        assert has_premium is False
    
    def test_has_premium_features_mixed(self, system):
        """Test premium feature detection with mixed features."""
        has_premium = system.has_premium_features(
            ["personal_training", "exclusive_facilities"]
        )
        assert has_premium is True
    
    def test_calculate_group_discount_single_member(self, system):
        """Test group discount calculation for single member."""
        discount, msg = system.calculate_group_discount(100, 1)
        assert discount == 0
        assert msg == ""
    
    def test_calculate_group_discount_two_members(self, system):
        """Test group discount calculation for two members."""
        discount, msg = system.calculate_group_discount(100, 2)
        assert discount == 10  # 10% of 100
        assert "Group discount" in msg
    
    def test_calculate_group_discount_multiple_members(self, system):
        """Test group discount calculation for multiple members."""
        discount, msg = system.calculate_group_discount(200, 5)
        assert discount == 20  # 10% of 200
    
    def test_calculate_special_offer_discount_under_200(self, system):
        """Test special offer discount for cost under $200."""
        discount, msg = system.calculate_special_offer_discount(150)
        assert discount == 0
        assert msg == ""
    
    def test_calculate_special_offer_discount_over_200(self, system):
        """Test special offer discount for cost over $200."""
        discount, msg = system.calculate_special_offer_discount(250)
        assert discount == 20
        assert ">$200" in msg
    
    def test_calculate_special_offer_discount_over_400(self, system):
        """Test special offer discount for cost over $400."""
        discount, msg = system.calculate_special_offer_discount(500)
        assert discount == 50
        assert ">$400" in msg
    
    def test_calculate_special_offer_discount_exactly_200(self, system):
        """Test special offer discount for cost exactly $200."""
        discount, msg = system.calculate_special_offer_discount(200)
        assert discount == 0
    
    def test_calculate_special_offer_discount_exactly_400(self, system):
        """Test special offer discount for cost exactly $400."""
        discount, msg = system.calculate_special_offer_discount(400)
        assert discount == 20  # Should get $20 discount, not $50
    
    def test_calculate_premium_surcharge_with_premium(self, system):
        """Test premium surcharge calculation when premium features are included."""
        surcharge, msg = system.calculate_premium_surcharge(100, True)
        assert surcharge == 15  # 15% of 100
        assert "Premium features" in msg
    
    def test_calculate_premium_surcharge_without_premium(self, system):
        """Test premium surcharge calculation when no premium features."""
        surcharge, msg = system.calculate_premium_surcharge(100, False)
        assert surcharge == 0
        assert msg == ""
    
    def test_calculate_total_cost_basic_no_features(self, system):
        """Test total cost calculation for basic membership with no features."""
        result = system.calculate_total_cost("basic", [], 1)
        assert result["valid"] is True
        assert result["base_cost"] == 50
        assert result["features_cost"] == 0
        assert result["total"] == 50
    
    def test_calculate_total_cost_premium_with_features(self, system):
        """Test total cost calculation for premium membership with features."""
        result = system.calculate_total_cost(
            "premium",
            ["personal_training", "group_classes"],
            1
        )
        assert result["valid"] is True
        assert result["base_cost"] == 100
        assert result["features_cost"] == 90  # 60 + 30
        assert result["subtotal"] == 190
        assert result["total"] == 190  # No discounts, no surcharge
    
    def test_calculate_total_cost_with_group_discount(self, system):
        """Test total cost calculation with group discount."""
        result = system.calculate_total_cost("premium", [], 2)
        assert result["valid"] is True
        assert result["base_cost"] == 100
        # Group discount: 10% of 100 = 10
        assert result["group_discount"] == 10
        assert result["total"] == 90
    
    def test_calculate_total_cost_with_special_offer_discount_200(self, system):
        """Test total cost calculation with special offer discount (>$200)."""
        # Create a scenario where total > 200
        result = system.calculate_total_cost(
            "family",
            ["personal_training", "group_classes", "nutrition_plan"],
            1
        )
        assert result["valid"] is True
        # Base: 150, Features: 60+30+40=130, Subtotal: 280
        # Special discount: $20
        assert result["subtotal"] > 200
        assert result["special_discount"] == 20
        assert result["total"] == 260  # 280 - 20
    
    def test_calculate_total_cost_with_special_offer_discount_400(self, system):
        """Test total cost calculation with special offer discount (>$400)."""
        # Create a scenario where total > 400
        result = system.calculate_total_cost(
            "family",
            ["personal_training", "exclusive_facilities", "specialized_training", "spa_access"],
            1
        )
        assert result["valid"] is True
        # Base: 150, Features: 60+80+100+70=310, Subtotal: 460
        # Premium surcharge: 15% of 460 = 69, Subtotal with surcharge: 529
        # Special discount: $50
        assert result["subtotal"] + result["premium_surcharge"] > 400
        assert result["special_discount"] == 50
        # Total should be: 460 + 69 - 50 = 479
        expected_total = result["subtotal"] + result["premium_surcharge"] - result["special_discount"]
        assert result["total"] == expected_total
    
    def test_calculate_total_cost_with_premium_surcharge(self, system):
        """Test total cost calculation with premium feature surcharge."""
        result = system.calculate_total_cost(
            "basic",
            ["exclusive_facilities"],
            1
        )
        assert result["valid"] is True
        # Base: 50, Features: 80, Subtotal: 130
        # Premium surcharge: 15% of 130 = 19 (rounded)
        assert result["premium_surcharge"] > 0
        assert "Premium features" in result["premium_msg"]
        # Total: 130 + 19 = 149
        expected_total = result["subtotal"] + result["premium_surcharge"]
        assert result["total"] == expected_total
    
    def test_calculate_total_cost_with_all_discounts(self, system):
        """Test total cost calculation with group discount and special offer."""
        result = system.calculate_total_cost(
            "family",
            ["personal_training", "group_classes", "nutrition_plan"],
            3  # Group of 3
        )
        assert result["valid"] is True
        # Base: 150, Features: 60+30+40=130, Subtotal: 280
        # Premium surcharge: 0 (no premium features)
        # Group discount: 10% of 280 = 28
        # Special discount: $20 (>$200)
        # Total: 280 - 28 - 20 = 232
        assert result["group_discount"] > 0
        assert result["special_discount"] > 0
        expected_total = (result["subtotal"] + result["premium_surcharge"] - 
                         result["group_discount"] - result["special_discount"])
        assert result["total"] == expected_total
    
    def test_calculate_total_cost_invalid_membership(self, system):
        """Test total cost calculation with invalid membership."""
        result = system.calculate_total_cost("invalid", [], 1)
        assert result["valid"] is False
        assert result["total"] == -1
        assert result["error"] is not None
    
    def test_calculate_total_cost_invalid_feature(self, system):
        """Test total cost calculation with invalid feature."""
        result = system.calculate_total_cost("basic", ["invalid_feature"], 1)
        assert result["valid"] is False
        assert result["total"] == -1
        assert result["error"] is not None
    
    def test_process_membership_confirmed(self, system):
        """Test processing membership when confirmed."""
        total = system.process_membership("basic", [], 1, confirmed=True)
        assert total == 50
    
    def test_process_membership_not_confirmed(self, system):
        """Test processing membership when not confirmed."""
        total = system.process_membership("basic", [], 1, confirmed=False)
        assert total == -1
    
    def test_process_membership_invalid(self, system):
        """Test processing membership with invalid selection."""
        total = system.process_membership("invalid", [], 1, confirmed=True)
        assert total == -1
    
    def test_calculate_total_cost_non_negative(self, system):
        """Test that total cost is never negative."""
        # Create scenario that might result in negative (should be clamped to 0)
        # This is more of a safety test
        result = system.calculate_total_cost("basic", [], 1)
        assert result["total"] >= 0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @pytest.fixture
    def system(self):
        """Fixture to create a GymMembershipSystem instance."""
        return GymMembershipSystem()
    
    def test_empty_feature_list(self, system):
        """Test with empty feature list."""
        result = system.calculate_total_cost("basic", [], 1)
        assert result["valid"] is True
        assert result["total"] == 50
    
    def test_large_group_size(self, system):
        """Test with very large group size."""
        result = system.calculate_total_cost("basic", [], 100)
        assert result["valid"] is True
        # Should still get 10% discount
        assert result["group_discount"] == 5  # 10% of 50
    
    def test_multiple_premium_features(self, system):
        """Test with multiple premium features."""
        result = system.calculate_total_cost(
            "basic",
            ["exclusive_facilities", "specialized_training", "spa_access"],
            1
        )
        assert result["valid"] is True
        # Should have premium surcharge
        assert result["premium_surcharge"] > 0
    
    def test_case_insensitive_membership(self, system):
        """Test that membership selection is case insensitive."""
        result1 = system.calculate_total_cost("BASIC", [], 1)
        result2 = system.calculate_total_cost("basic", [], 1)
        assert result1["total"] == result2["total"]
    
    def test_case_insensitive_features(self, system):
        """Test that feature selection is case insensitive."""
        result1 = system.calculate_total_cost("basic", ["PERSONAL_TRAINING"], 1)
        result2 = system.calculate_total_cost("basic", ["personal_training"], 1)
        assert result1["total"] == result2["total"]
