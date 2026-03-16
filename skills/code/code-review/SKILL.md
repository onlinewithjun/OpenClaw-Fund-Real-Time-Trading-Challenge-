---
name: code-review
description: Systematic code review patterns covering security, performance, maintainability, correctness, and testing with severity levels, structured feedback guidance, review process, and anti-patterns to avoid. Use when reviewing PRs, establishing review standards, or improving review quality.
author: wpank
version: 1.0.0
---

# Code Review Skill

## Overview

This skill provides systematic code review patterns covering:
- **Security** - Vulnerability detection and secure coding practices
- **Performance** - Efficiency optimizations and bottleneck identification
- **Maintainability** - Code clarity, modularity, and documentation
- **Correctness** - Logic errors and edge case handling
- **Testing** - Test coverage and quality assurance

## Usage

Use this skill when:
1. Reviewing pull requests before merge
2. Establishing team code review standards
3. Improving overall code review quality
4. Training new developers on review best practices

## Review Process

### Step 1: Initial Assessment
- Understand the PR scope and objectives
- Identify affected components and dependencies
- Check for related issues or requirements

### Step 2: Systematic Review
Review code against each category:

| Category | Focus Areas |
|----------|-------------|
| Security | Input validation, authentication, authorization, data protection |
| Performance | Algorithm complexity, database queries, caching, resource usage |
| Maintainability | Naming, structure, comments, documentation, modularity |
| Correctness | Logic flow, edge cases, error handling, null checks |
| Testing | Unit tests, integration tests, coverage, test quality |

### Step 3: Severity Classification

Classify findings by severity:

- **Critical** - Must fix before merge (security vulnerabilities, data loss)
- **High** - Should fix before merge (major bugs, performance issues)
- **Medium** - Fix in follow-up (code quality, maintainability)
- **Low** - Nice to have (style, minor improvements)

### Step 4: Structured Feedback

Provide feedback in this format:

```markdown
## [Severity] Category: Issue Title

**Location**: `file/path.ext:line-number`

**Problem**: Clear description of the issue

**Impact**: What could go wrong

**Suggestion**: Concrete fix recommendation

**Example**:
```language
// Before
problematic code

// After
fixed code
```
```

## Anti-Patterns to Avoid

❌ **Vague comments**: "This looks wrong"
✅ **Specific feedback**: "This loop is O(n²), consider using a hash map"

❌ **Personal criticism**: "You should have known better"
✅ **Constructive guidance**: "Consider using the existing utility function"

❌ **Nitpicking style**: Focus on formatting over substance
✅ **Prioritize impact**: Focus on security, correctness, performance

## Integration

This skill works well with:
- `pr-review` - Automated PR workflow
- `security-auditor` - Deep security analysis
- `test-case-generator` - Generate missing tests
- `review-summarizer` - Summarize large reviews

## References

- Google Code Review Guidelines
- Microsoft Engineering System
- GitHub PR Review Best Practices
