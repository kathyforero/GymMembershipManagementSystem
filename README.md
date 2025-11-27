# Gym Membership Management System

A command-line application for managing gym memberships with cost calculations, discounts, and comprehensive validation.

## Features

- **Membership Plans**: Basic, Premium, and Family memberships with different benefits and costs
- **Additional Features**: Add extra features like personal training, group classes, and premium facilities
- **Cost Calculation**: Automatic calculation of base costs, feature costs, and total
- **Group Discounts**: 10% discount when 2 or more members sign up together
- **Special Offer Discounts**: 
  - $20 discount if total cost exceeds $200
  - $50 discount if total cost exceeds $400
- **Premium Feature Surcharge**: 15% surcharge on total cost when premium features are included
- **Validation**: Comprehensive validation of membership and feature selections
- **User Confirmation**: Summary display before finalizing membership
- **Error Handling**: Clear error messages for invalid inputs

## Assumptions

1. **Membership Plans**:
   - Basic: $50/month - Access to gym facilities, locker room, basic equipment
   - Premium: $100/month - All Basic benefits + premium equipment, priority booking, nutrition consultation
   - Family: $150/month - All Premium benefits + up to 4 family members, family classes, childcare

2. **Additional Features**:
   - Standard Features:
     - Personal Training Sessions: $60
     - Group Classes: $30
     - Custom Nutrition Plan: $40
   - Premium Features (15% surcharge applies):
     - Exclusive Facilities Access: $80
     - Specialized Training Programs: $100
     - Spa and Wellness Access: $70

3. **Discount Rules**:
   - Group discount (10%) is applied to the subtotal (base + features + premium surcharge)
   - Special offer discounts are applied after premium surcharge but can stack with group discount
   - Premium surcharge (15%) is applied to the subtotal before discounts
   - All discounts are applied in the order: premium surcharge → group discount → special offer discount

4. **Cost Calculation Order**:
   1. Base membership cost
   2. Additional features cost
   3. Subtotal = base + features
   4. Premium surcharge (if premium features included) = 15% of subtotal
   5. Subtotal with surcharge = subtotal + premium surcharge
   6. Group discount (if 2+ members) = 10% of subtotal with surcharge
   7. Special offer discount (if applicable)
   8. Final total = subtotal with surcharge - group discount - special offer discount

5. **Output**:
   - Returns total cost as a positive integer if membership is confirmed and valid
   - Returns -1 if input is invalid or membership is canceled

6. **Validation**:
   - Membership and feature selections are case-insensitive
   - All memberships and features are available by default (can be set to unavailable for testing)
   - Empty feature lists are allowed

## Installation

1. Ensure you have Python 3.7 or higher installed
2. Activate the virtual environment:
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```
3. No external packages are required (uses only Python standard library)

## Usage

### Running the Application

```bash
python gym_membership.py
```

The application will guide you through:
1. Selecting a membership plan
2. Choosing additional features (optional)
3. Entering group size
4. Reviewing the summary
5. Confirming or canceling the membership

### Example Session

```
============================================================
WELCOME TO THE GYM MEMBERSHIP MANAGEMENT SYSTEM
============================================================

============================================================
AVAILABLE MEMBERSHIP PLANS
============================================================

Basic Membership - $50/month [✓ Available]
Benefits:
  • Access to gym facilities
  • Locker room access
  • Basic equipment usage

Premium Membership - $100/month [✓ Available]
Benefits:
  • All Basic benefits
  • Access to premium equipment
  • Priority booking
  • Nutrition consultation

Family Membership - $150/month [✓ Available]
Benefits:
  • All Premium benefits
  • Up to 4 family members
  • Family fitness classes
  • Childcare services

Select a membership plan (basic/premium/family): premium

[Features displayed...]

Enter feature keys separated by commas (or press Enter for none):
Features: personal_training,group_classes

Enter number of members in group (minimum 1): 2

💡 You qualify for a 10% group discount for 2 members!

============================================================
MEMBERSHIP SUMMARY
============================================================

Membership Plan: Premium
Base Cost: $100

Additional Features:
  • Personal Training Sessions
  • Group Classes
Features Cost: $90

Subtotal: $190

Group discount (10% for 2 members): -$19
Special offer discount (>$200): -$20

============================================================
TOTAL COST: $151
============================================================

Confirm this membership? (yes/no): yes

✅ Membership confirmed! Total cost: $151
```

## Running Tests

Run all unit tests:

```bash
python -m unittest test_gym_membership.py -v
```

Or using pytest (if installed):

```bash
pytest test_gym_membership.py -v
```

## Design Patterns Applied

The codebase has been refactored using several design patterns to improve maintainability, extensibility, and reduce code duplication:

### 1. **Abstract Base Classes (ABC)**
- `Validator`: Abstract interface for validation strategies
- `PriceModifier`: Abstract interface for price modifications (discounts/surcharges)
- `DisplayComponent`: Abstract interface for display components

### 2. **Strategy Pattern**
- **Validators**: `MembershipValidator` and `FeatureValidator` implement different validation strategies
- **Price Modifiers**: `PremiumSurchargeModifier`, `GroupDiscountModifier`, and `SpecialOfferModifier` implement different pricing strategies
- **Display Components**: `MembershipDisplay`, `FeatureDisplay`, and `SummaryDisplay` implement different display strategies

### 3. **Factory Pattern**
- `MembershipFactory`: Centralized creation of membership plans
- `FeatureFactory`: Centralized creation of additional features
- Makes it easy to add new memberships or features without modifying existing code

### 4. **Chain of Responsibility Pattern**
- Price modifiers are applied in sequence, each checking if it can apply and then modifying the price
- Allows easy addition of new discount/surcharge types without modifying existing code

### 5. **Data Classes**
- `MembershipPlan` and `AdditionalFeature` use `@dataclass` for cleaner, more maintainable code
- `CalculationContext` provides structured context for calculations

### Benefits:
- **Reduced Code**: Better organization reduces complexity
- **Extensibility**: Easy to add new memberships, features, discounts, or display formats
- **Testability**: Each component can be tested independently
- **Maintainability**: Clear separation of concerns makes code easier to understand and modify

## Project Structure

```
GymMembershipManagementSystem/
├── models.py                  # Data models (MembershipPlan, AdditionalFeature, FeatureType)
├── validators.py              # Validation classes (Validator base + implementations)
├── modifiers.py               # Price modifiers (PriceModifier base + implementations + Chain)
├── factories.py               # Factory classes (MembershipFactory, FeatureFactory)
├── display.py                 # Display components (DisplayComponent base + implementations)
├── gym_membership.py          # Main application (orchestrates all components)
├── test_gym_membership.py     # Unit tests (46 tests, all passing)
├── __init__.py                # Package initialization
├── requirements.txt           # Dependencies (none required)
├── README.md                  # This file
└── .venv/                     # Virtual environment
```

### Architecture Overview

The codebase follows **Separation of Concerns** principle with modular architecture:

- **models.py**: Pure data classes, no business logic
- **validators.py**: Validation logic with Strategy pattern (base class + implementations)
- **modifiers.py**: Price modification logic with Strategy + Chain of Responsibility
- **factories.py**: Object creation logic (Factory pattern)
- **display.py**: Presentation logic (Strategy pattern)
- **gym_membership.py**: Orchestration layer, coordinates all components

Each module has a single responsibility and can be tested independently.

## Testing

The project includes comprehensive unit tests covering:
- Membership plan validation
- Feature validation
- Cost calculations
- Discount calculations (group, special offers)
- Premium surcharge calculations
- Edge cases and boundary conditions
- Error handling

All 46 tests pass successfully.

## API Usage (Programmatic)

You can also use the system programmatically:

```python
from gym_membership import GymMembershipSystem

system = GymMembershipSystem()

# Calculate total cost
result = system.calculate_total_cost(
    membership_key="premium",
    feature_keys=["personal_training", "group_classes"],
    group_size=2
)

if result["valid"]:
    print(f"Total cost: ${result['total']}")
else:
    print(f"Error: {result['error']}")

# Process membership
total = system.process_membership(
    membership_key="premium",
    feature_keys=["personal_training"],
    group_size=1,
    confirmed=True
)
```

## Error Handling

The system handles various error scenarios:
- Invalid membership type selection
- Invalid feature selection
- Unavailable memberships or features
- Invalid group size input
- Calculation errors

All errors return descriptive messages and a return value of -1.

## License

This project is provided as-is for educational and demonstration purposes.
