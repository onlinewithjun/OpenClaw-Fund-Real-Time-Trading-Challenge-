---
name: code-simplifier
description: Simplify and refactor code to reduce complexity, improve readability, and maintain functionality. Supports C++, Python, JavaScript, TypeScript, Java, and more.
author: openclaw
version: 1.0.0
---

# Code Simplifier Skill

## Overview

Automated code simplification and refactoring that:
- **Reduces Complexity**: Lower cyclomatic complexity, simplify conditionals
- **Improves Readability**: Better naming, structure, comments
- **Eliminates Duplication**: DRY principle, extract functions
- **Maintains Functionality**: Preserve behavior, ensure tests pass
- **Optimizes Structure**: Better modularity, separation of concerns

## Supported Languages

| Language | Refactoring Depth | Features |
|----------|------------------|----------|
| C++ | Deep | Function extraction, class restructuring, template simplification |
| Python | Deep | Function extraction, decorator optimization, comprehension conversion |
| JavaScript/TypeScript | Deep | Arrow functions, destructuring, async/await conversion |
| Java | Medium | Method extraction, stream API, lambda conversion |
| Go | Medium | Function simplification, error handling patterns |
| Rust | Medium | Pattern matching, Result/Option chaining |

## Refactoring Categories

### 1. Complexity Reduction

| Pattern | Before | After |
|---------|--------|-------|
| Nested Conditionals | Deep if-else nesting | Early returns, guard clauses |
| Complex Loops | Multi-purpose loops | Split into focused functions |
| Long Methods | 100+ line functions | Extracted helper functions |
| Boolean Logic | Complex conditions | Extracted boolean methods |

### 2. Code Duplication

| Pattern | Detection | Solution |
|---------|-----------|----------|
| Copy-Paste Code | Identical code blocks | Extract common function |
| Similar Logic | Same pattern, different data | Template/parameterized function |
| Repeated Conditions | Same condition checks | Extracted condition method |
| Duplicate Constants | Magic numbers/strings | Named constants |

### 3. Readability Improvements

| Aspect | Improvement |
|--------|-------------|
| Naming | Descriptive variable/function names |
| Structure | Logical code organization |
| Comments | Clarify intent, remove obvious comments |
| Formatting | Consistent style, proper spacing |
| Type Hints | Add type annotations where helpful |

### 4. Modernization

| Language | Modernization |
|----------|---------------|
| C++ | Raw pointers → smart pointers, C-style casts → named casts |
| Python | Python 2 → 3, loops → comprehensions |
| JavaScript | Callbacks → Promises → async/await, var → let/const |
| Java | Loops → streams, anonymous classes → lambdas |

## Usage

### Simplify a File

```bash
# Basic simplification
Simplify this code: src/utils.cpp

# Specific focus
Reduce complexity in: data_processor.py

# Aggressive refactoring
Refactor for readability: api/handlers.ts
```

### Simplify a Function

```bash
# Target specific function
Simplify the `calculateRevenue` function in: finance.cpp

# Extract large function
Break down this 200-line function: report_generator.py
```

### Batch Simplification

```bash
# All files in directory
Simplify all C++ files in: src/utils/

# Specific pattern
Refactor all *.test.ts files: tests/
```

## Refactoring Process

### Step 1: Analysis

- Calculate cyclomatic complexity
- Identify code smells
- Detect duplication
- Analyze dependencies

### Step 2: Plan Refactoring

Prioritize changes:
1. **Critical**: Bugs, security issues, performance problems
2. **High**: High complexity (>15), long methods (>50 lines)
3. **Medium**: Moderate complexity (10-15), some duplication
4. **Low**: Naming, formatting, minor improvements

### Step 3: Apply Refactoring

**Safe Refactorings** (automated):
- Rename variables/functions
- Extract methods
- Inline trivial methods
- Move methods between classes
- Replace temp with query

**Careful Refactorings** (review required):
- Change function signatures
- Modify class hierarchies
- Change data structures
- Optimize algorithms

### Step 4: Verification

- Run existing tests
- Check behavior preservation
- Validate performance
- Review complexity metrics

## Refactoring Patterns

### Pattern 1: Extract Function

**Before**:
```cpp
void processOrder(Order& order) {
    // ... 20 lines of validation ...
    if (order.items.empty()) { /* ... */ }
    if (order.customer.id <= 0) { /* ... */ }
    if (order.totalAmount < 0) { /* ... */ }
    // ... 30 lines of processing ...
    double subtotal = 0;
    for (const auto& item : order.items) {
        subtotal += item.price * item.quantity;
    }
    // ... 50 lines of payment ...
}
```

**After**:
```cpp
void processOrder(Order& order) {
    validateOrder(order);
    calculateSubtotal(order);
    processPayment(order);
}

bool validateOrder(const Order& order) {
    if (order.items.empty()) {
        throw InvalidOrderException("Empty items");
    }
    if (order.customer.id <= 0) {
        throw InvalidOrderException("Invalid customer");
    }
    if (order.totalAmount < 0) {
        throw InvalidOrderException("Negative amount");
    }
    return true;
}
```

### Pattern 2: Replace Nested Conditional with Guard Clauses

**Before**:
```python
def calculate_discount(customer, order):
    if customer.is_premium:
        if order.total > 1000:
            if order.items_count > 5:
                return 0.20
            else:
                return 0.15
        else:
            return 0.10
    else:
        if order.total > 500:
            return 0.05
        else:
            return 0.0
```

**After**:
```python
def calculate_discount(customer, order):
    if not customer.is_premium:
        return 0.05 if order.total > 500 else 0.0
    
    if order.total <= 1000:
        return 0.10
    
    return 0.20 if order.items_count > 5 else 0.15
```

### Pattern 3: Replace Magic Numbers with Constants

**Before**:
```cpp
if (temperature > 100 && temperature < 200) {
    pressure = 3.14159 * radius * radius;
    timeout = 30000;
}
```

**After**:
```cpp
constexpr double MIN_OPERATING_TEMP = 100.0;
constexpr double MAX_OPERATING_TEMP = 200.0;
constexpr double PI = 3.14159;
constexpr int CONNECTION_TIMEOUT_MS = 30000;

if (temperature > MIN_OPERATING_TEMP && temperature < MAX_OPERATING_TEMP) {
    pressure = PI * radius * radius;
    timeout = CONNECTION_TIMEOUT_MS;
}
```

### Pattern 4: Simplify Boolean Logic

**Before**:
```java
if (user != null && user.isActive() && 
    user.getSubscription() != null && 
    user.getSubscription().isValid() &&
    (user.getRole() == Role.ADMIN || user.getRole() == Role.MODERATOR)) {
    return true;
}
return false;
```

**After**:
```java
boolean canModerate() {
    if (user == null || !user.isActive()) return false;
    if (user.getSubscription() == null || !user.getSubscription().isValid()) return false;
    return user.getRole() == Role.ADMIN || user.getRole() == Role.MODERATOR;
}
```

## Metrics

### Complexity Targets

| Metric | Good | Needs Work | Critical |
|--------|------|------------|----------|
| Cyclomatic Complexity | <10 | 10-20 | >20 |
| Function Length | <30 lines | 30-100 lines | >100 lines |
| Nesting Depth | <3 levels | 3-5 levels | >5 levels |
| Parameter Count | <5 | 5-7 | >7 |

### Improvement Tracking

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Cyclomatic Complexity | 25 | 8 | -68% |
| Lines of Code | 350 | 280 | -20% |
| Duplicate Code | 45% | 5% | -89% |
| Test Coverage | 60% | 85% | +42% |

## Integration

Works with:
- `code-review` - Review refactored code
- `test-case-generator` - Generate tests before refactoring
- `security-auditor` - Ensure security not compromised
- `pr-review` - Submit refactoring PRs

## Best Practices

1. **Test First**: Ensure tests exist before refactoring
2. **Small Steps**: One refactoring at a time
3. **Commit Often**: Each successful refactoring = one commit
4. **Preserve Behavior**: Functionality must not change
5. **Measure Impact**: Track complexity metrics

## Commands

| Command | Description |
|---------|-------------|
| `simplify-code <file>` | Simplify a code file |
| `extract-function <file> <function>` | Extract function from code |
| `reduce-complexity <file>` | Focus on complexity reduction |
| `remove-duplication <dir>` | Find and eliminate duplicate code |
| `modernize-code <file>` | Update to modern language features |

## Safety Guidelines

### Safe to Automate
- Rename identifiers
- Reformat code
- Extract pure functions
- Inline trivial functions
- Reorder imports/includes

### Require Review
- Change public APIs
- Modify class hierarchies
- Change data structures
- Optimize performance-critical code
- Alter error handling

### Never Automate
- Business logic changes
- Security-critical code
- Performance bottlenecks (without profiling)
- Code without tests

## Examples

### C++ Example

**Before**:
```cpp
int processData(std::vector<int> data, bool flag1, bool flag2) {
    int result = 0;
    for (int i = 0; i < data.size(); i++) {
        if (data[i] > 0) {
            if (flag1) {
                result += data[i] * 2;
            } else {
                result += data[i];
            }
        } else {
            if (flag2) {
                result -= data[i];
            }
        }
    }
    return result;
}
```

**After**:
```cpp
int processPositiveValue(int value, bool flag) {
    return flag ? value * 2 : value;
}

int processData(std::vector<int> data, bool flag1, bool flag2) {
    return std::accumulate(data.begin(), data.end(), 0,
        [flag1, flag2](int sum, int value) {
            if (value > 0) return sum + processPositiveValue(value, flag1);
            if (flag2) return sum - value;
            return sum;
        });
}
```

### Python Example

**Before**:
```python
def get_user_data(user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        data = {}
        data['id'] = user.id
        data['name'] = user.name
        data['email'] = user.email
        data['created'] = user.created_at
        return data
    else:
        return None
```

**After**:
```python
@dataclass
class UserData:
    id: int
    name: str
    email: str
    created: datetime

def get_user_data(user_id: int) -> Optional[UserData]:
    user = db.get(User, user_id)
    return UserData(user.id, user.name, user.email, user.created_at) if user else None
```
