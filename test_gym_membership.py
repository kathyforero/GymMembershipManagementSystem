"""
Unit tests for the Gym Membership Management System.
"""

import unittest
from gym_membership import GymMembershipSystem
from models import MembershipPlan, AdditionalFeature, FeatureType


class TestMembershipPlan(unittest.TestCase):
    """Test cases for MembershipPlan class."""
    
    def test_membership_plan_creation(self):
        """Test creating a membership plan."""
        plan = MembershipPlan("Basic", 50, ["Access to gym"], True)
        self.assertEqual(plan.name, "Basic")
        self.assertEqual(plan.cost, 50)
        self.assertEqual(len(plan.benefits), 1)
        self.assertTrue(plan.available)
    
    def test_membership_plan_str(self):
        """Test string representation of membership plan."""
        plan = MembershipPlan("Premium", 100, ["Benefits"], True)
        self.assertIn("Premium", str(plan))
        self.assertIn("100", str(plan))


class TestAdditionalFeature(unittest.TestCase):
    """Test cases for AdditionalFeature class."""
    
    def test_feature_creation(self):
        """Test creating an additional feature."""
        feature = AdditionalFeature("Personal Training", 60, FeatureType.STANDARD, True)
        self.assertEqual(feature.name, "Personal Training")
        self.assertEqual(feature.cost, 60)
        self.assertEqual(feature.feature_type, FeatureType.STANDARD)
        self.assertTrue(feature.available)


class TestGymMembershipSystem(unittest.TestCase):
    """Test cases for GymMembershipSystem class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.system = GymMembershipSystem()
    
    def test_initialization(self):
        """Test system initialization."""
        self.assertIsNotNone(self.system.membership_plans)
        self.assertIsNotNone(self.system.additional_features)
        self.assertIn("basic", self.system.membership_plans)
        self.assertIn("premium", self.system.membership_plans)
        self.assertIn("family", self.system.membership_plans)
    
    def test_validate_membership_selection_valid(self):
        """Test validation of valid membership selection."""
        is_valid, error = self.system.validate_membership_selection("basic")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_membership_selection_invalid_key(self):
        """Test validation of invalid membership key."""
        is_valid, error = self.system.validate_membership_selection("invalid")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_membership_selection_unavailable(self):
        """Test validation of unavailable membership."""
        # Make a plan unavailable
        self.system.membership_plans["basic"].available = False
        is_valid, error = self.system.validate_membership_selection("basic")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        # Restore for other tests
        self.system.membership_plans["basic"].available = True
    
    def test_validate_feature_selection_valid(self):
        """Test validation of valid feature selection."""
        is_valid, error, features = self.system.validate_feature_selection(["personal_training"])
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        self.assertEqual(len(features), 1)
    
    def test_validate_feature_selection_invalid_key(self):
        """Test validation of invalid feature key."""
        is_valid, error, features = self.system.validate_feature_selection(["invalid_feature"])
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        self.assertEqual(len(features), 0)
    
    def test_validate_feature_selection_unavailable(self):
        """Test validation of unavailable feature."""
        # Make a feature unavailable
        self.system.additional_features["personal_training"].available = False
        is_valid, error, features = self.system.validate_feature_selection(["personal_training"])
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        # Restore for other tests
        self.system.additional_features["personal_training"].available = True
    
    def test_validate_feature_selection_multiple(self):
        """Test validation of multiple features."""
        is_valid, error, features = self.system.validate_feature_selection(
            ["personal_training", "group_classes"]
        )
        self.assertTrue(is_valid)
        self.assertEqual(len(features), 2)
    
    def test_calculate_base_cost(self):
        """Test base cost calculation."""
        cost = self.system.calculate_base_cost("basic")
        self.assertEqual(cost, 50)
        
        cost = self.system.calculate_base_cost("premium")
        self.assertEqual(cost, 100)
        
        cost = self.system.calculate_base_cost("family")
        self.assertEqual(cost, 150)
    
    def test_calculate_features_cost_single(self):
        """Test feature cost calculation for single feature."""
        cost = self.system.calculate_features_cost(["personal_training"])
        self.assertEqual(cost, 60)
    
    def test_calculate_features_cost_multiple(self):
        """Test feature cost calculation for multiple features."""
        cost = self.system.calculate_features_cost(["personal_training", "group_classes"])
        self.assertEqual(cost, 90)  # 60 + 30
    
    def test_calculate_features_cost_empty(self):
        """Test feature cost calculation for no features."""
        cost = self.system.calculate_features_cost([])
        self.assertEqual(cost, 0)
    
    def test_has_premium_features_true(self):
        """Test premium feature detection when premium features are present."""
        has_premium = self.system.has_premium_features(["exclusive_facilities"])
        self.assertTrue(has_premium)
    
    def test_has_premium_features_false(self):
        """Test premium feature detection when no premium features are present."""
        has_premium = self.system.has_premium_features(["personal_training", "group_classes"])
        self.assertFalse(has_premium)
    
    def test_has_premium_features_mixed(self):
        """Test premium feature detection with mixed features."""
        has_premium = self.system.has_premium_features(
            ["personal_training", "exclusive_facilities"]
        )
        self.assertTrue(has_premium)
    
    def test_calculate_group_discount_single_member(self):
        """Test group discount calculation for single member."""
        discount, msg = self.system.calculate_group_discount(100, 1)
        self.assertEqual(discount, 0)
        self.assertEqual(msg, "")
    
    def test_calculate_group_discount_two_members(self):
        """Test group discount calculation for two members."""
        discount, msg = self.system.calculate_group_discount(100, 2)
        self.assertEqual(discount, 10)  # 10% of 100
        self.assertIn("Group discount", msg)
    
    def test_calculate_group_discount_multiple_members(self):
        """Test group discount calculation for multiple members."""
        discount, msg = self.system.calculate_group_discount(200, 5)
        self.assertEqual(discount, 20)  # 10% of 200
    
    def test_calculate_special_offer_discount_under_200(self):
        """Test special offer discount for cost under $200."""
        discount, msg = self.system.calculate_special_offer_discount(150)
        self.assertEqual(discount, 0)
        self.assertEqual(msg, "")
    
    def test_calculate_special_offer_discount_over_200(self):
        """Test special offer discount for cost over $200."""
        discount, msg = self.system.calculate_special_offer_discount(250)
        self.assertEqual(discount, 20)
        self.assertIn(">$200", msg)
    
    def test_calculate_special_offer_discount_over_400(self):
        """Test special offer discount for cost over $400."""
        discount, msg = self.system.calculate_special_offer_discount(500)
        self.assertEqual(discount, 50)
        self.assertIn(">$400", msg)
    
    def test_calculate_special_offer_discount_exactly_200(self):
        """Test special offer discount for cost exactly $200."""
        discount, msg = self.system.calculate_special_offer_discount(200)
        self.assertEqual(discount, 0)
    
    def test_calculate_special_offer_discount_exactly_400(self):
        """Test special offer discount for cost exactly $400."""
        discount, msg = self.system.calculate_special_offer_discount(400)
        self.assertEqual(discount, 20)  # Should get $20 discount, not $50
    
    def test_calculate_premium_surcharge_with_premium(self):
        """Test premium surcharge calculation when premium features are included."""
        surcharge, msg = self.system.calculate_premium_surcharge(100, True)
        self.assertEqual(surcharge, 15)  # 15% of 100
        self.assertIn("Premium features", msg)
    
    def test_calculate_premium_surcharge_without_premium(self):
        """Test premium surcharge calculation when no premium features."""
        surcharge, msg = self.system.calculate_premium_surcharge(100, False)
        self.assertEqual(surcharge, 0)
        self.assertEqual(msg, "")
    
    def test_calculate_total_cost_basic_no_features(self):
        """Test total cost calculation for basic membership with no features."""
        result = self.system.calculate_total_cost("basic", [], 1)
        self.assertTrue(result["valid"])
        self.assertEqual(result["base_cost"], 50)
        self.assertEqual(result["features_cost"], 0)
        self.assertEqual(result["total"], 50)
    
    def test_calculate_total_cost_premium_with_features(self):
        """Test total cost calculation for premium membership with features."""
        result = self.system.calculate_total_cost(
            "premium",
            ["personal_training", "group_classes"],
            1
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["base_cost"], 100)
        self.assertEqual(result["features_cost"], 90)  # 60 + 30
        self.assertEqual(result["subtotal"], 190)
        self.assertEqual(result["total"], 190)  # No discounts, no surcharge
    
    def test_calculate_total_cost_with_group_discount(self):
        """Test total cost calculation with group discount."""
        result = self.system.calculate_total_cost("premium", [], 2)
        self.assertTrue(result["valid"])
        self.assertEqual(result["base_cost"], 100)
        # Group discount: 10% of 100 = 10
        self.assertEqual(result["group_discount"], 10)
        self.assertEqual(result["total"], 90)
    
    def test_calculate_total_cost_with_special_offer_discount_200(self):
        """Test total cost calculation with special offer discount (>$200)."""
        # Create a scenario where total > 200
        result = self.system.calculate_total_cost(
            "family",
            ["personal_training", "group_classes", "nutrition_plan"],
            1
        )
        self.assertTrue(result["valid"])
        # Base: 150, Features: 60+30+40=130, Subtotal: 280
        # Special discount: $20
        self.assertGreater(result["subtotal"], 200)
        self.assertEqual(result["special_discount"], 20)
        self.assertEqual(result["total"], 260)  # 280 - 20
    
    def test_calculate_total_cost_with_special_offer_discount_400(self):
        """Test total cost calculation with special offer discount (>$400)."""
        # Create a scenario where total > 400
        result = self.system.calculate_total_cost(
            "family",
            ["personal_training", "exclusive_facilities", "specialized_training", "spa_access"],
            1
        )
        self.assertTrue(result["valid"])
        # Base: 150, Features: 60+80+100+70=310, Subtotal: 460
        # Premium surcharge: 15% of 460 = 69, Subtotal with surcharge: 529
        # Special discount: $50
        self.assertGreater(result["subtotal"] + result["premium_surcharge"], 400)
        self.assertEqual(result["special_discount"], 50)
        # Total should be: 460 + 69 - 50 = 479
        expected_total = result["subtotal"] + result["premium_surcharge"] - result["special_discount"]
        self.assertEqual(result["total"], expected_total)
    
    def test_calculate_total_cost_with_premium_surcharge(self):
        """Test total cost calculation with premium feature surcharge."""
        result = self.system.calculate_total_cost(
            "basic",
            ["exclusive_facilities"],
            1
        )
        self.assertTrue(result["valid"])
        # Base: 50, Features: 80, Subtotal: 130
        # Premium surcharge: 15% of 130 = 19 (rounded)
        self.assertGreater(result["premium_surcharge"], 0)
        self.assertIn("Premium features", result["premium_msg"])
        # Total: 130 + 19 = 149
        expected_total = result["subtotal"] + result["premium_surcharge"]
        self.assertEqual(result["total"], expected_total)
    
    def test_calculate_total_cost_with_all_discounts(self):
        """Test total cost calculation with group discount and special offer."""
        result = self.system.calculate_total_cost(
            "family",
            ["personal_training", "group_classes", "nutrition_plan"],
            3  # Group of 3
        )
        self.assertTrue(result["valid"])
        # Base: 150, Features: 60+30+40=130, Subtotal: 280
        # Premium surcharge: 0 (no premium features)
        # Group discount: 10% of 280 = 28
        # Special discount: $20 (>$200)
        # Total: 280 - 28 - 20 = 232
        self.assertGreater(result["group_discount"], 0)
        self.assertGreater(result["special_discount"], 0)
        expected_total = (result["subtotal"] + result["premium_surcharge"] - 
                         result["group_discount"] - result["special_discount"])
        self.assertEqual(result["total"], expected_total)
    
    def test_calculate_total_cost_invalid_membership(self):
        """Test total cost calculation with invalid membership."""
        result = self.system.calculate_total_cost("invalid", [], 1)
        self.assertFalse(result["valid"])
        self.assertEqual(result["total"], -1)
        self.assertIsNotNone(result["error"])
    
    def test_calculate_total_cost_invalid_feature(self):
        """Test total cost calculation with invalid feature."""
        result = self.system.calculate_total_cost("basic", ["invalid_feature"], 1)
        self.assertFalse(result["valid"])
        self.assertEqual(result["total"], -1)
        self.assertIsNotNone(result["error"])
    
    def test_process_membership_confirmed(self):
        """Test processing membership when confirmed."""
        total = self.system.process_membership("basic", [], 1, confirmed=True)
        self.assertEqual(total, 50)
    
    def test_process_membership_not_confirmed(self):
        """Test processing membership when not confirmed."""
        total = self.system.process_membership("basic", [], 1, confirmed=False)
        self.assertEqual(total, -1)
    
    def test_process_membership_invalid(self):
        """Test processing membership with invalid selection."""
        total = self.system.process_membership("invalid", [], 1, confirmed=True)
        self.assertEqual(total, -1)
    
    def test_calculate_total_cost_non_negative(self):
        """Test that total cost is never negative."""
        # Create scenario that might result in negative (should be clamped to 0)
        # This is more of a safety test
        result = self.system.calculate_total_cost("basic", [], 1)
        self.assertGreaterEqual(result["total"], 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.system = GymMembershipSystem()
    
    def test_empty_feature_list(self):
        """Test with empty feature list."""
        result = self.system.calculate_total_cost("basic", [], 1)
        self.assertTrue(result["valid"])
        self.assertEqual(result["total"], 50)
    
    def test_large_group_size(self):
        """Test with very large group size."""
        result = self.system.calculate_total_cost("basic", [], 100)
        self.assertTrue(result["valid"])
        # Should still get 10% discount
        self.assertEqual(result["group_discount"], 5)  # 10% of 50
    
    def test_multiple_premium_features(self):
        """Test with multiple premium features."""
        result = self.system.calculate_total_cost(
            "basic",
            ["exclusive_facilities", "specialized_training", "spa_access"],
            1
        )
        self.assertTrue(result["valid"])
        # Should have premium surcharge
        self.assertGreater(result["premium_surcharge"], 0)
    
    def test_case_insensitive_membership(self):
        """Test that membership selection is case insensitive."""
        result1 = self.system.calculate_total_cost("BASIC", [], 1)
        result2 = self.system.calculate_total_cost("basic", [], 1)
        self.assertEqual(result1["total"], result2["total"])
    
    def test_case_insensitive_features(self):
        """Test that feature selection is case insensitive."""
        result1 = self.system.calculate_total_cost("basic", ["PERSONAL_TRAINING"], 1)
        result2 = self.system.calculate_total_cost("basic", ["personal_training"], 1)
        self.assertEqual(result1["total"], result2["total"])


if __name__ == "__main__":
    unittest.main()

