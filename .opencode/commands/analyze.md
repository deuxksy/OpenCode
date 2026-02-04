---
description: 코드베이스 분석
template: Analyze the codebase structure, dependencies, and suggest improvements.
---

## Codebase Analysis

### Structure Overview

Analyze the project to understand:

1. **File Organization**
   - Main source files and their purposes
   - Configuration files
   - Documentation structure
   - Testing setup

2. **Dependencies**
   - External packages in requirements.txt
   - Development dependencies
   - Version constraints
   - Security vulnerabilities

3. **Code Quality**
   - Adherence to PEP 8
   - Type hints coverage
   - Documentation quality
   - Test coverage

4. **Architecture**
   - Component relationships
   - Data flow
   - Design patterns used
   - Potential coupling issues

### Analysis Commands

**Check dependencies:**
```bash
pip list
pip check
```

**Find Python files:**
```bash
find . -name "*.py" -not -path "./.venv/*" -not -path "./.opencode/node_modules/*"
```

**Count lines of code:**
```bash
find . -name "*.py" -not -path "./.venv/*" | xargs wc -l
```

### Improvement Suggestions

Look for:

1. **Code Smells**
   - Long functions (>50 lines)
   - Duplicate code
   - Dead code
   - Overly complex logic

2. **Unused Code**
   - Unused imports
   - Unused functions
   - Commented-out code

3. **Security Issues**
   - Hardcoded credentials
   - Insecure dependencies
   - Unsafe practices

4. **Performance**
   - Inefficient algorithms
   - Unnecessary computations
   - Memory leaks

### Report Format

Provide analysis in sections:
1. **Project Overview** - High-level summary
2. **Strengths** - What's done well
3. **Areas for Improvement** - Specific recommendations
4. **Priority Issues** - Critical items to address
5. **Next Steps** - Actionable recommendations
