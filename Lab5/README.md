# Lab 5: Static Code Analysis — Car Rental System

## 1. Objective

The purpose of this lab was to analyze the original `car_rental.py` program using **Pylint**, **Bandit**, and **Flake8**, identify security vulnerabilities and code-quality problems, correct the identified issues, and rerun the tools to verify the improvements.

The original program contained:

- Unsafe SQL queries
- Dynamic code execution
- Insecure receipt-file handling
- Weak hashing
- A hardcoded administrator password
- Missing input validation
- Style violations

## 2. Issues Identified and Fixes Applied

The table below summarizes the significant issues found during the initial analysis and how each was addressed. Security issues are listed first, with high- and medium-severity findings prioritized.

| # | Issue | Type | Location in original file | Description | Fix Approach |
|---|-------|------|---------------------------|-------------|--------------|
| 1 | Overly permissive file permissions | Security — High (Bandit B103) | `writeReceipt()`; `os.chmod(path, 0o777)` | The program changed receipt permissions to `0o777`, granting excessive permissions to the file owner, group, and others. | Removed the permission change and used a securely created temporary file with its default restrictive permissions. |
| 2 | Weak licence hashing | Security — High (Bandit B324) | `licenceHash()`; `hashlib.sha1(...)` | SHA-1 is considered unsuitable for security-sensitive cryptographic use. | Replaced SHA-1 with SHA-256 and explicitly encoded the licence string as UTF-8. |
| 3 | Unsafe dynamic code execution | Security — Medium (Bandit B102) | `applyPromo()`; `exec(rule, {}, scope)` | The program executed a promotion rule as Python code. If untrusted input reached this function, arbitrary code could run. | Removed `exec()` and allowed only the explicitly supported `"10%"` promotion rule. |
| 4 | SQL injection in customer registration | Security — Medium (Bandit B608) | `registerCustomer()`; formatted `INSERT` query | Customer data was inserted into an SQL statement using string formatting, creating an SQL-injection risk. | Replaced string formatting with parameterized SQL using `?` placeholders and a tuple of values. |
| 5 | SQL injection in customer lookup | Security — Medium (Bandit B608) | `findCustomer()`; concatenated `SELECT` query | The customer name was concatenated directly into the SQL query. Crafted input could alter the query conditions. | Used a parameterized `SELECT` query so the customer name is treated as data rather than SQL code. |
| 6 | Insecure temporary-file creation | Security — Medium (Bandit B306) | `writeReceipt()`; `tempfile.mktemp()` | `mktemp()` returns a temporary filename without securely creating the file, allowing a potential race condition. | Replaced it with `tempfile.mkstemp()` and managed the opened file using a context manager with UTF-8 encoding. |
| 7 | Hardcoded administrator password | Security | `adminLogin()`; default password and comparison | The administrator password was embedded in the source code, making it easy to discover and reuse. | Read the expected password from the `CAR_RENTAL_ADMIN_PASSWORD` environment variable and used `secrets.compare_digest()` for comparison. |
| 8 | Weak booking-code randomness | Security — Low (Bandit B311) | `bookingCode()`; `random.randint(...)` | The standard pseudo-random generator is not intended for security-sensitive identifiers and may make booking codes easier to predict. | Replaced it with `secrets.token_hex()` to generate a harder-to-predict booking identifier. |
| 9 | Mutable default argument | Code quality | `addCar()`; `features=[]` | A mutable list as a default argument can be shared across calls and cause unexpected state changes. | Changed the default to `None` and created a fresh list for each call. |
| 10 | Bare exception handler | Code quality | `returnCar()`; `except: pass` | Catching every exception and ignoring it could hide programming errors and invalid input. | Added explicit validation for unknown cars and negative distances, and raised `ValueError` for invalid operations. |
| 11 | Invalid rental dates | Logic | `rentCar()`; date subtraction and cost calculation | The original function did not reject an end date that was earlier than or equal to the start date, potentially producing invalid rental charges. | Validated the rental duration and rejected periods with zero or negative days. |
| 12 | Invalid or unavailable car rentals | Logic | `rentCar()`; fleet access and booking creation | The original function did not check that the car existed or was available before creating a booking. | Added checks for unknown cars and unavailable vehicles, and marked a car unavailable after a successful booking. |
| 13 | Negative daily rental rate | Logic | `addCar()`; fleet insertion | A negative daily rate could result in a negative rental cost. | Added validation that rejects negative daily rates. |
| 14 | Inconsistent naming and missing documentation | Code quality (Pylint) | Multiple functions | CamelCase function names and missing docstrings made the code less consistent and harder to maintain. | Renamed functions using `snake_case` and added module and function docstrings. |
| 15 | Long lines and trailing whitespace | Style (Flake8) | Multiple locations | Lines exceeding the configured length limit and whitespace on blank lines violated Python style checks. | Reformatted long statements across multiple lines and removed trailing whitespace. |
| 16 | Unused import and other style issues | Code quality (Pylint/Flake8) | Original imports and multiple locations | Unused imports and other style violations added unnecessary clutter and reduced readability. | Removed the unused `json` import and corrected the reported formatting and style issues. |

> **Note:** Line references use the original, unmodified `car_rental.py` and identify the relevant functions or statements. Line numbers may differ after edits. Severity labels are based on the original Bandit findings where a Bandit rule is specified; logic and style findings are categorized separately.

## 3. Verification After Fixes

After updating the program, Pylint, Bandit, and Flake8 were rerun against the final `car_rental.py` file.

| Tool | Initial result | Final result |
|------|----------------|--------------|
| Pylint | 4.94/10 | 10.00/10 |
| Bandit | 2 High, 4 Medium, and 5 Low severity findings | No issues identified |
| Flake8 | Multiple style violations | No findings |

The final program also passed Python compilation and ran successfully:

- The customer lookup injection test returned an empty result.
- The rental-date validation prevented invalid rental periods.
- The updated promotion function rejected unsupported rules.

## 4. Conclusion

The lab demonstrated how static-analysis tools can reveal security vulnerabilities, coding-standard violations, and maintainability problems. The updated program uses:

- Parameterized SQL queries
- Safer temporary-file creation
- SHA-256 hashing
- Secure booking-code generation
- Restricted promotion rules
- Input validation
- Consistent naming

The final results show a Pylint score of 10.00/10, no issues identified by Bandit, and no findings from Flake8. These results indicate a substantial improvement in code quality and address the major issues identified during the initial analysis.
