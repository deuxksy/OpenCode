---
description: pytest로 테스트 실행
template: Run the full test suite with pytest and show coverage report. Focus on failing tests and suggest fixes.
---

## Run Tests with pytest

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

### Command Explanation

- `pytest tests/` - Run all tests in the tests directory
- `-v` - Verbose mode, show detailed output
- `--cov=.` - Calculate code coverage for current directory
- `--cov-report=term-missing` - Show missing lines in terminal

### Analysis

After running tests:

1. **Check for Failures**: Identify which tests failed and why
2. **Review Coverage**: Look for untested code paths
3. **Suggest Fixes**: Provide specific recommendations for fixing failing tests
4. **Best Practices**: Ensure tests follow pytest conventions

### Common Issues

- Missing test dependencies
- Incorrect test assertions
- Tests not isolating properly
- Mock/stub setup issues
