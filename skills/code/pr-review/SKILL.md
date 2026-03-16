---
name: pr-review
description: Automated Pull Request review workflow with GitHub integration. Reviews PRs, posts comments, manages labels, and integrates with CI/CD pipelines.
author: openclaw
version: 1.0.0
---

# PR Review Skill

## Overview

Automated Pull Request review workflow that integrates with GitHub to:
- Review PR code changes automatically
- Post structured feedback as comments
- Manage PR labels and assignments
- Integrate with CI/CD pipelines
- Track review status and approvals

## Prerequisites

- GitHub Personal Access Token (PAT) with `repo` scope
- GitHub CLI (`gh`) installed and authenticated
- Repository access permissions

## Setup

### Step 1: Configure GitHub Token

```bash
# Set environment variable
$env:GITHUB_TOKEN="ghp_your_token_here"

# Or add to openclaw.json env section
```

### Step 2: Authenticate GitHub CLI

```bash
gh auth login
gh auth status
```

## Usage

### Review a Specific PR

```bash
# Provide PR URL or number
Review this PR: https://github.com/owner/repo/pull/123
```

### Review Recent PRs

```bash
# Review all open PRs in a repository
Review all open PRs in owner/repo
```

### Automated Review Workflow

1. **Fetch PR Details**
   - PR title, description, author
   - Changed files and diff
   - CI/CD status

2. **Code Analysis**
   - Run `code-review` skill on changes
   - Check for security issues
   - Verify test coverage
   - Validate coding standards

3. **Post Feedback**
   - Add inline comments on specific lines
   - Post summary comment with overall assessment
   - Apply appropriate labels
   - Request changes or approve

4. **Follow-up**
   - Track addressed feedback
   - Re-review updated code
   - Final approval decision

## Output Format

### Summary Comment Template

```markdown
## Code Review Summary

**Reviewer**: @assistant
**Review Date**: YYYY-MM-DD
**Overall Status**: ✅ Approved / ⚠️ Changes Requested / 📝 Under Review

### Changes Overview
- Files changed: X
- Lines added: +Y
- Lines removed: -Z

### Key Findings

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Detailed Feedback

See inline comments for specific suggestions.

### Checklist
- [ ] Security reviewed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Performance considered
- [ ] Coding standards followed
```

## Integration

Works with:
- `code-review` - Detailed code analysis
- `security-auditor` - Security scanning
- `test-case-generator` - Generate missing tests
- `ci-cd-integration` - Pipeline status checks

## Commands

| Command | Description |
|---------|-------------|
| `review-pr <url>` | Review specific PR |
| `list-open-prs <repo>` | List open PRs in repository |
| `review-status <pr>` | Check review status |
| `approve-pr <pr>` | Approve PR |
| `request-changes <pr>` | Request changes |

## Best Practices

1. **Be Constructive**: Focus on code, not the author
2. **Be Specific**: Reference exact lines and suggest fixes
3. **Prioritize**: Address critical issues first
4. **Be Timely**: Review within 24 hours
5. **Follow-up**: Re-review promptly after updates

## Security Notes

- Never commit tokens or secrets
- Verify PR source before reviewing
- Check for suspicious code patterns
- Validate external dependencies
