---
name: security-auditor
description: Comprehensive security auditing for codebases. Detects vulnerabilities, security anti-patterns, and compliance issues. Supports multiple languages and security standards (OWASP, CWE, SANS).
author: openclaw
version: 1.0.0
---

# Security Auditor Skill

## Overview

Comprehensive security auditing tool that detects:
- **Vulnerabilities**: SQL injection, XSS, CSRF, buffer overflows, etc.
- **Security Anti-Patterns**: Hardcoded secrets, weak cryptography, insecure configurations
- **Compliance Issues**: OWASP Top 10, CWE/SANS Top 25, PCI-DSS, GDPR
- **Code Quality**: Security-focused code smells and best practices

## Supported Languages

| Language | Analysis Depth | Frameworks |
|----------|---------------|------------|
| C/C++ | Deep (memory safety, buffer overflows) | STL, POSIX |
| Python | Deep (injection, deserialization) | Django, Flask, FastAPI |
| JavaScript/TypeScript | Deep (XSS, prototype pollution) | Node.js, React, Vue |
| Java | Deep (injection, deserialization) | Spring, Hibernate |
| Go | Medium (injection, concurrency) | Standard library |
| Rust | Medium (memory safety, unsafe blocks) | Standard library |

## Security Categories

### 1. Injection Vulnerabilities

| Type | Detection | Severity |
|------|-----------|----------|
| SQL Injection | String concatenation in queries | Critical |
| Command Injection | Unsanitized shell commands | Critical |
| LDAP Injection | Unescaped LDAP queries | High |
| XPath Injection | Dynamic XPath expressions | High |

### 2. Cross-Site Scripting (XSS)

| Type | Detection | Severity |
|------|-----------|----------|
| Reflected XSS | Unescaped user input in output | High |
| Stored XSS | Unsanitized data in database | Critical |
| DOM-based XSS | Unsafe DOM manipulation | Medium |

### 3. Authentication & Authorization

| Issue | Detection | Severity |
|-------|-----------|----------|
| Weak Password Hashing | MD5, SHA1 for passwords | High |
| Missing Authentication | Protected routes without auth | Critical |
| Broken Authorization | IDOR, privilege escalation | Critical |
| Session Management | Insecure cookies, session fixation | High |

### 4. Cryptography

| Issue | Detection | Severity |
|-------|-----------|----------|
| Weak Algorithms | DES, RC4, MD5 | High |
| Hardcoded Keys | Keys in source code | Critical |
| Insecure Random | Non-crypto RNG for security | Medium |
| Missing Encryption | Sensitive data in plaintext | High |

### 5. Memory Safety (C/C++)

| Issue | Detection | Severity |
|-------|-----------|----------|
| Buffer Overflow | Unsafe string functions | Critical |
| Use After Free | Dangling pointers | Critical |
| Memory Leak | Unfreed allocations | Medium |
| Integer Overflow | Unchecked arithmetic | High |

### 6. Configuration Security

| Issue | Detection | Severity |
|-------|-----------|----------|
| Debug Mode in Production | Debug flags enabled | High |
| Verbose Errors | Stack traces exposed | Medium |
| Insecure Headers | Missing security headers | Medium |
| CORS Misconfiguration | Overly permissive CORS | High |

## Usage

### Audit a File

```bash
# Single file security audit
Audit security: src/auth.cpp

# Specific category
Check for injection vulnerabilities in: api/handlers.py
```

### Audit a Directory

```bash
# Full project audit
Security audit: ./src/

# Specific language
Audit all Python files: ./backend/ --lang=python
```

### Compliance Check

```bash
# OWASP Top 10 compliance
Check OWASP compliance: ./webapp/

# CWE/SANS Top 25
Check CWE compliance: ./core/
```

## Audit Process

### Step 1: Static Analysis

- Parse source code AST
- Build control flow graph
- Identify data flow paths
- Detect dangerous patterns

### Step 2: Pattern Matching

- Match against vulnerability signatures
- Check for security anti-patterns
- Validate secure coding practices
- Identify compliance gaps

### Step 3: Risk Assessment

- Evaluate exploitability
- Assess impact severity
- Consider context and mitigations
- Assign risk scores

### Step 4: Report Generation

Generate structured report with:
- Vulnerability description
- Location (file:line)
- Severity rating (CVSS)
- Remediation guidance
- Code examples

## Output Format

### Security Audit Report

```markdown
# Security Audit Report

**Project**: project-name
**Date**: YYYY-MM-DD
**Auditor**: security-auditor v1.0.0
**Files Scanned**: 42
**Issues Found**: 15

## Summary

| Severity | Count |
|----------|-------|
| Critical | 2 |
| High | 5 |
| Medium | 6 |
| Low | 2 |

## Critical Issues

### [CRITICAL] SQL Injection in User Authentication

**Location**: `src/auth.cpp:127`

**CWE**: CWE-89 (SQL Injection)
**OWASP**: A03:2021 - Injection

**Description**:
User input is directly concatenated into SQL query without sanitization.

**Vulnerable Code**:
```cpp
std::string query = "SELECT * FROM users WHERE username='" + username + "'";
```

**Exploit Scenario**:
Attacker can bypass authentication by providing username: `' OR '1'='1`

**Remediation**:
Use parameterized queries:
```cpp
auto query = db.prepare("SELECT * FROM users WHERE username = ?");
query.bind(1, username);
```

**References**:
- https://owasp.org/www-community/attacks/SQL_Injection
- https://cwe.mitre.org/data/definitions/89.html

## High Severity Issues

### [HIGH] Hardcoded API Key

**Location**: `src/config.py:15`

**CWE**: CWE-798 (Hardcoded Credentials)

**Description**:
API key is hardcoded in source code.

**Vulnerable Code**:
```python
API_KEY = "sk-1234567890abcdef"
```

**Remediation**:
Use environment variables or secure secret management:
```python
import os
API_KEY = os.environ.get("API_KEY")
```

## Recommendations

1. **Immediate**: Fix all Critical and High severity issues
2. **Short-term**: Implement secure coding training
3. **Long-term**: Add security scanning to CI/CD pipeline
```

## Severity Ratings

| Rating | CVSS Score | Action Required |
|--------|------------|-----------------|
| Critical | 9.0-10.0 | Fix immediately, block deployment |
| High | 7.0-8.9 | Fix within 7 days |
| Medium | 4.0-6.9 | Fix within 30 days |
| Low | 0.1-3.9 | Fix when convenient |

## Integration

Works with:
- `code-review` - Include security in code reviews
- `pr-review` - Automated security checks in PRs
- `ci-cd-integration` - Gate deployments on security issues
- `dependency-checker` - Scan third-party vulnerabilities

## Compliance Standards

| Standard | Coverage |
|----------|----------|
| OWASP Top 10 (2021) | 100% |
| CWE/SANS Top 25 | 100% |
| PCI-DSS | Partial |
| HIPAA | Partial |
| GDPR | Partial |
| SOC 2 | Partial |

## Best Practices

1. **Shift Left**: Audit early in development cycle
2. **Automate**: Integrate into CI/CD pipeline
3. **Prioritize**: Fix critical issues first
4. **Educate**: Train developers on secure coding
5. **Re-audit**: Regular security assessments

## Commands

| Command | Description |
|---------|-------------|
| `security-audit <path>` | Full security audit |
| `check-injection <path>` | Check injection vulnerabilities |
| `check-auth <path>` | Audit authentication/authorization |
| `check-crypto <path>` | Audit cryptography usage |
| `compliance-check <standard> <path>` | Compliance verification |

## Limitations

- Static analysis only (no runtime analysis)
- May produce false positives
- Cannot detect business logic flaws
- Requires code access (no binary analysis)

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE/SANS Top 25: https://cwe.mitre.org/top25/
- Secure Coding Guidelines: Language-specific best practices
