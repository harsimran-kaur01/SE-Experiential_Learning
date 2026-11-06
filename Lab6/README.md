# Lab 6: Code and Branch Coverage Analysis — Course Registration

## About

This lab focuses on measuring and improving code coverage and branch coverage using Python's `coverage.py` tool and `pytest`.

The application is a small Python module that:
- Determines whether a student can register for a course.
- Calculates waitlist positions.
- Calculates late registration fees.

## Objectives

- Understand the difference between code coverage and branch coverage.
- Measure test coverage using Python Coverage.py.
- Identify untested statements and decision branches.
- Write test cases for normal conditions and edge cases.
- Achieve at least 90% code and branch coverage.

## Code Coverage vs. Branch Coverage

### Code (Statement) Coverage

Code coverage measures the percentage of executable statements that are executed during testing.

It helps identify statements that have not been tested.

### Branch Coverage

Branch coverage measures whether each possible outcome of a decision, such as True and False conditions in an `if` statement, has been executed.

It helps identify untested decision paths.

### Key Difference

A program can achieve 100% statement coverage without achieving 100% branch coverage. This happens when statements are executed but not every possible decision outcome is tested.

Branch coverage therefore provides additional information about the completeness of test cases.

## Coverage Results

### Code Coverage

- Total tests: 17
- Tests passed: 17
- Statements: 32
- Missed statements: 0
- Code coverage: **100%**

### Branch Coverage

- Total tests: 24
- Tests passed: 24
- Statements: 32
- Missed statements: 0
- Branches: 24
- Partial branches: 0
- Branch coverage: **100%**

Both coverage measurements exceed the required minimum of 90%.

## Files

| File | Description |
|---|---|
| `course_registration.py` | Application module under test |
| `test_course_registration.py` | Original starter test file |
| `CodeCoverageTest_PES1UG24CS187_course_registration.py` | Additional tests for code coverage |
| `BranchCoverageTest_PES1UG24CS187_course_registration.py` | Additional tests for branch coverage |
| `screenshots/Code_coverage_100percent.png` | Terminal screenshot showing 100% code coverage |
| `screenshots/BranchCoverage_100percent.png` | Terminal screenshot showing 100% branch coverage |

## Commands Used

### Run Code Coverage Tests

```bash
python -m coverage erase
python -m coverage run --source=course_registration -m pytest -p no:cacheprovider CodeCoverageTest_PES1UG24CS187_course_registration.py
python -m coverage report -m
```

### Run Branch Coverage Tests

```bash
python -m coverage erase
python -m coverage run --branch --source=course_registration -m pytest -p no:cacheprovider BranchCoverageTest_PES1UG24CS187_course_registration.py
python -m coverage report -m
```

## Conclusion

The course registration application was tested using separate code coverage and branch coverage test suites.

The final results achieved were:

- **100% Code Coverage**
- **100% Branch Coverage**

All 17 code coverage tests and all 24 branch coverage tests passed successfully.

This exercise demonstrates how additional test cases can improve test completeness by covering executable statements, decision outcomes, and edge cases.