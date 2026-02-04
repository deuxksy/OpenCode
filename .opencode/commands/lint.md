---
description: 코드 린팅 및 포맷팅
template: Run black, isort, and mypy to format code and check for issues. Report any errors and suggest fixes.
---

## Code Linting and Formatting

### Step 1: Format with Black

```bash
black . --line-length 100
```

Black is the uncompromising Python code formatter. It automatically:
- Formats code to PEP 8 standards
- Normalizes whitespace
- Handles line wrapping at 100 characters

### Step 2: Organize Imports with isort

```bash
isort . --profile black
```

isort organizes Python imports in the correct order:
1. Standard library imports
2. Third-party imports
3. Local application imports

### Step 3: Type Check with mypy

```bash
mypy .
```

mypy performs static type checking:
- Validates type hints
- Catches type errors before runtime
- Improves code reliability

### All-in-One Command

```bash
black . && isort . && mypy .
```

### Analysis

After running linting tools:

1. **Report Formatting Changes**: What was reformatted?
2. **Identify Type Errors**: Any type checking issues?
3. **Suggest Improvements**: Code quality recommendations
4. **Check Violations**: PEP 8 compliance status

### Common Issues

- Missing type hints
- Incorrect import ordering
- Line length violations
- Unused imports
- Type annotation errors
