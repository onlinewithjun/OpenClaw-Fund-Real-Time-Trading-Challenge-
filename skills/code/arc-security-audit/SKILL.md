---
name: arc-security-audit
description: Comprehensive security audit for an agent's full skill stack. Analyzes installed skills for vulnerabilities, permission issues, and security anti-patterns.
author: trypto1019
version: 1.0.0
---

# ARC Security Audit Skill

## Overview

Comprehensive security audit for AI agent skill stacks:
- **Skill Analysis**: Scan all installed skills for security issues
- **Permission Audit**: Check skill permissions and access levels
- **Vulnerability Detection**: Identify known security vulnerabilities
- **Anti-Pattern Detection**: Find security anti-patterns in skill code
- **Risk Assessment**: Provide risk scores and remediation guidance

## Audit Categories

### 1. Skill Code Security

| Check | Description | Severity |
|-------|-------------|----------|
| Hardcoded Secrets | API keys, passwords in skill code | Critical |
| Unsafe Exec | Unsanitized shell command execution | Critical |
| Path Traversal | Unsafe file path handling | High |
| Injection Risks | SQL, command, template injection | High |
| Insecure Downloads | HTTP without TLS verification | Medium |

### 2. Permission Analysis

| Check | Description | Severity |
|-------|-------------|----------|
| Elevated Permissions | Skills requiring admin/root access | High |
| Network Access | Unrestricted outbound connections | Medium |
| File System Access | Broad file system permissions | Medium |
| External APIs | Unverified third-party API calls | Medium |

### 3. Dependency Security

| Check | Description | Severity |
|-------|-------------|----------|
| Outdated Packages | Dependencies with known vulnerabilities | High |
| Unmaintained deps | Abandoned dependencies | Medium |
| Supply Chain | Dependencies from untrusted sources | High |

### 4. Behavioral Security

| Check | Description | Severity |
|-------|-------------|----------|
| Data Exfiltration | Skills sending data to unknown endpoints | Critical |
| Persistence | Skills creating persistent backdoors | Critical |
| Privilege Escalation | Skills attempting to elevate privileges | Critical |

## Usage

### Full Security Audit

```bash
# Audit entire skill stack
Perform security audit on all installed skills

# Audit specific skill
Audit security of: code-review skill
```

### Targeted Audits

```bash
# Check for hardcoded secrets
Scan for hardcoded secrets in skills

# Check permissions
Audit skill permissions and access levels

# Check dependencies
Scan skill dependencies for vulnerabilities
```

## Audit Process

### Step 1: Inventory

- List all installed skills
- Catalog skill locations and versions
- Identify skill dependencies

### Step 2: Static Analysis

- Parse skill SKILL.md files
- Analyze embedded scripts and code
- Check for dangerous patterns

### Step 3: Permission Mapping

- Map skill permissions to capabilities
- Identify over-privileged skills
- Check permission boundaries

### Step 4: Risk Scoring

- Calculate risk scores per skill
- Aggregate stack-level risk
- Prioritize remediation

## Output Format

### Security Audit Report

```markdown
# ARC Security Audit Report

**Date**: YYYY-MM-DD
**Skills Audited**: 58
**Issues Found**: 12

## Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 5 |
| Low | 5 |

## Critical Issues

None found.

## High Severity Issues

### [HIGH] Hardcoded API Key Pattern Detected

**Skill**: some-skill
**Location**: SKILL.md:45
**Pattern**: `API_KEY = "sk-..."`
**Recommendation**: Use environment variables
```

## Risk Scoring

| Score | Level | Action |
|-------|-------|--------|
| 9-10 | Critical | Remove skill immediately |
| 7-8 | High | Review and remediate |
| 4-6 | Medium | Monitor and plan fix |
| 1-3 | Low | Accept or improve |
| 0 | None | No issues |

## Integration

Works with:
- `security-auditor` - Code-level security analysis
- `arc-skill-gitops` - Remove/rollback risky skills
- `code-review` - Review skill code changes

## Best Practices

1. **Regular Audits**: Run security audit monthly
2. **Before Install**: Audit new skills before installation
3. **After Update**: Re-audit skills after updates
4. **Incident Response**: Audit after security incidents

## Commands

| Command | Description |
|---------|-------------|
| `arc-security-audit` | Full skill stack audit |
| `arc-security-audit --skill=<name>` | Audit specific skill |
| `arc-security-audit --quick` | Quick scan (critical only) |
| `arc-security-audit --report` | Generate detailed report |
