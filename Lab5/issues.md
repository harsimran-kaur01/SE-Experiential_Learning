# Lab 5: Static Code Analysis — Issue Summary

The original code was analyzed using **Pylint**, **Bandit**, and **Flake8**. Issues are listed below in order of security impact (High severity first).

## Issues Found and Fixes

| # | Issue | Type | Location | Description | Fix Approach |
|---|-------|------|----------|-------------|--------------|
| 1 | Overly permissive file permissions | Security — High | `writeReceipt()` | Setting permissions to `0o777` allowed excessive access to the receipt file. | Removed the permission change and retained secure temporary-file defaults. |
| 2 | Weak licence hashing | Security — High | `licenceHash()` | SHA-1 is no longer recommended for security-sensitive hashing. | Replaced SHA-1 with SHA-256. |
| 3 | Hardcoded administrator password | Security | `adminLogin()` | A password embedded in source code could be exposed to anyone who can read the file. | Read the expected password from an environment variable and used `secrets.compare_digest()`. |
| 4 | Unsafe dynamic code execution | Security — Medium | `applyPromo()` | `exec()` could execute arbitrary Python code supplied as a promotion rule. | Removed `exec()` and allowed only the supported `"10%"` promotion. |
| 5 | SQL injection | Security — Medium | `registerCustomer()`, `findCustomer()` | SQL queries included user input directly, allowing query manipulation. | Used parameterized SQL queries with `?` placeholders. |
| 6 | Insecure temporary file creation | Security — Medium | `writeReceipt()` | `tempfile.mktemp()` could expose a race condition when creating receipt files. | Used `tempfile.mkstemp()` and a file context manager. |
| 7 | Mutable default argument | Code quality | `addCar()` | A default empty list could be shared between function calls. | Used `features=None` and created a new list when needed. |
| 8 | Bare exception handler | Code quality | `returnCar()` | Silently ignoring all exceptions could hide errors. | Added explicit validation and raised `ValueError` for invalid cars or distances. |
| 9 | Missing validation for rental dates | Logic | `rentCar()` | Invalid rental periods, including end dates before start dates, could produce incorrect charges. | Validated that the rental duration is positive. |
| 10 | Style and naming issues | Code quality | Multiple functions | Inconsistent naming, long lines, and missing documentation reduced readability. | Used snake_case names, docstrings, and formatting corrections. |

## Summary

The cleaned code uses:

- Parameterized SQL queries
- Safer temporary-file handling
- Stronger hashing (SHA-256)
- Restricted promotion rules
- Input validation
- Clearer function names

## Final Analysis Results

| Tool | Result |
|------|--------|
| Pylint | 10.00/10 |
| Bandit | No issues reported |
| Flake8 | No issues reported |
