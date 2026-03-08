---
name: test-case-generator
description: Generate comprehensive unit tests for code files. Supports multiple languages (C++, Python, JavaScript, TypeScript, Java) with various testing frameworks.
author: openclaw
version: 1.0.0
---

# Test Case Generator Skill

## Overview

Automatically generate comprehensive unit tests for code files with support for:
- **Multiple Languages**: C++, Python, JavaScript, TypeScript, Java, Go
- **Testing Frameworks**: GoogleTest, pytest, Jest, JUnit, and more
- **Test Types**: Unit tests, integration tests, edge cases, property-based tests
- **Coverage Analysis**: Identify untested code paths

## Supported Languages & Frameworks

| Language | Frameworks | File Extension |
|----------|------------|----------------|
| C++ | GoogleTest, Catch2, doctest | `.cpp`, `.cc` |
| Python | pytest, unittest | `.py` |
| JavaScript | Jest, Mocha, Jasmine | `.js`, `.jsx` |
| TypeScript | Jest, Vitest | `.ts`, `.tsx` |
| Java | JUnit 5, TestNG | `.java` |
| Go | testing, testify | `.go` |

## Usage

### Generate Tests for a File

```bash
# Specify target file
Generate unit tests for: src/utils.cpp

# Specify framework
Generate pytest tests for: data_processor.py
```

### Generate Tests for a Directory

```bash
# All source files in directory
Generate tests for all C++ files in: src/

# Specific pattern
Generate tests for *.ts files in: components/
```

## Test Generation Process

### Step 1: Analyze Source Code

- Identify functions/methods to test
- Understand input/output types
- Detect dependencies and mocks needed
- Analyze control flow and branches

### Step 2: Generate Test Cases

For each function, generate:

1. **Happy Path Tests**
   - Normal input scenarios
   - Expected output verification

2. **Edge Case Tests**
   - Boundary conditions
   - Empty/null inputs
   - Maximum values

3. **Error Handling Tests**
   - Exception scenarios
   - Invalid inputs
   - Failure modes

4. **Integration Tests** (when applicable)
   - Multi-function workflows
   - External dependency interactions

### Step 3: Create Test File

```cpp
// Example: C++ GoogleTest
#include <gtest/gtest.h>
#include "src/utils.h"

// Test case: Normal operation
TEST(UtilsTest, CalculateSum_ReturnsCorrectResult) {
    // Arrange
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    
    // Act
    int result = Utils::calculateSum(numbers);
    
    // Assert
    EXPECT_EQ(result, 15);
}

// Test case: Edge case - empty input
TEST(UtilsTest, CalculateSum_EmptyVector_ReturnsZero) {
    // Arrange
    std::vector<int> numbers = {};
    
    // Act
    int result = Utils::calculateSum(numbers);
    
    // Assert
    EXPECT_EQ(result, 0);
}

// Test case: Error handling
TEST(UtilsTest, CalculateSum_NegativeNumbers_ThrowsException) {
    // Arrange
    std::vector<int> numbers = {-1, -2, -3};
    
    // Act & Assert
    EXPECT_THROW(Utils::calculateSum(numbers), std::invalid_argument);
}
```

## Output Structure

```
project/
├── src/
│   ├── utils.cpp
│   └── utils.h
└── tests/
    ├── utils_test.cpp      # Generated test file
    ├── CMakeLists.txt      # Test build configuration
    └── README.md           # Test execution instructions
```

## Configuration

### Test Generation Options

| Option | Description | Default |
|--------|-------------|---------|
| `framework` | Testing framework to use | Auto-detect |
| `coverage` | Generate coverage-focused tests | true |
| `mocks` | Generate mock objects | true |
| `comments` | Add explanatory comments | true |
| `naming` | Test naming convention | descriptive |

### Example Configuration

```json
{
  "testGenerator": {
    "framework": "gtest",
    "outputDir": "tests/",
    "naming": "ClassName_MethodName_Scenario",
    "includeCoverage": true,
    "generateFixtures": true
  }
}
```

## Quality Metrics

Generated tests aim for:
- **Coverage**: ≥80% line coverage
- **Assertions**: 2-5 assertions per test
- **Independence**: Each test is isolated
- **Repeatability**: Deterministic results
- **Readability**: Clear test names and structure

## Integration

Works with:
- `code-review` - Review generated tests
- `test-runner` - Execute generated tests
- `ci-cd-integration` - Add to CI pipeline
- `coverage-analyzer` - Measure test coverage

## Best Practices

1. **Review Before Committing**: Always review generated tests
2. **Add Business Logic**: Supplement with domain-specific tests
3. **Maintain Tests**: Update tests as code evolves
4. **Mock External Dependencies**: Isolate unit under test
5. **Test Behavior, Not Implementation**: Focus on what, not how

## Commands

| Command | Description |
|---------|-------------|
| `generate-tests <file>` | Generate tests for a file |
| `generate-tests <dir> --lang=<lang>` | Generate tests for directory |
| `update-tests <file>` | Update existing tests |
| `check-coverage <file>` | Analyze test coverage |

## Examples

### C++ Example

**Input**: `src/calculator.cpp`

**Output**: `tests/calculator_test.cpp`

```cpp
TEST(CalculatorTest, Add_TwoPositiveNumbers_ReturnsSum) {
    Calculator calc;
    EXPECT_EQ(calc.add(5, 3), 8);
}

TEST(CalculatorTest, Add_NegativeNumbers_ReturnsCorrectResult) {
    Calculator calc;
    EXPECT_EQ(calc.add(-5, -3), -8);
}

TEST(CalculatorTest, Divide_ByZero_ThrowsException) {
    Calculator calc;
    EXPECT_THROW(calc.divide(10, 0), DivisionByZeroException);
}
```

### Python Example

**Input**: `src/data_processor.py`

**Output**: `tests/test_data_processor.py`

```python
import pytest
from src.data_processor import DataProcessor

def test_process_valid_data():
    processor = DataProcessor()
    result = processor.process([1, 2, 3])
    assert result == 6

def test_process_empty_list():
    processor = DataProcessor()
    result = processor.process([])
    assert result == 0

def test_process_invalid_type():
    processor = DataProcessor()
    with pytest.raises(TypeError):
        processor.process("invalid")
```
