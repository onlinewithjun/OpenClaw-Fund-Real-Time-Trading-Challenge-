---
name: alex-session-wrap-up
description: End-of-session automation that commits unpushed work, extracts learnings, detects patterns, and persists rules. Automatic session summary and knowledge capture.
author: xbillwatsonx
version: 1.0.0
---

# Alex Session Wrap-Up

## Overview

Automatic end-of-session automation:
- **Work Commitment**: Commit and push unpushed changes
- **Learning Extraction**: Capture lessons learned
- **Pattern Detection**: Identify recurring patterns
- **Rule Persistence**: Save new rules and preferences
- **Session Summary**: Generate comprehensive summary

## Automation Tasks

### 1. Code Commitment

| Task | Description |
|------|-------------|
| Detect Changes | Find uncommitted files |
| Stage Changes | Stage relevant files |
| Commit | Create descriptive commit |
| Push | Push to remote repository |

### 2. Knowledge Capture

| Task | Description |
|------|-------------|
| Extract Learnings | Capture new insights |
| Document Decisions | Record key decisions |
| Save Patterns | Store detected patterns |
| Update Memory | Persist to memory files |

### 3. Session Summary

| Task | Description |
|------|-------------|
| Task Summary | List completed tasks |
| Time Tracking | Track session duration |
| Skill Usage | List skills used |
| Output Summary | Summarize deliverables |

## Usage

### Manual Trigger

```bash
# End session and wrap up
Wrap up current session

# End session with custom notes
Wrap up session with notes: "Completed security audit"
```

### Automatic Trigger

```bash
# Configure auto wrap-up
Enable automatic session wrap-up

# Set wrap-up time
Schedule wrap-up at: 18:00 daily
```

## Wrap-Up Process

### Step 1: Detect Work

```bash
# Check git status
git status

# Check for unsaved files
Find modified files

# Check session history
Review session tasks
```

### Step 2: Commit Changes

```bash
# Stage changes
git add .

# Create commit
git commit -m "Session work: [auto-generated summary]"

# Push to remote
git push
```

### Step 3: Extract Learnings

```markdown
## Session Learnings

### Technical Discoveries
- [New technical insight 1]
- [New technical insight 2]

### Process Improvements
- [Workflow improvement 1]
- [Workflow improvement 2]

### Issues Encountered
- [Issue 1] → [Resolution]
- [Issue 2] → [Resolution]
```

### Step 4: Detect Patterns

```markdown
## Detected Patterns

### Recurring Tasks
- Task X performed 5 times
- Skill Y used in 80% of sessions

### Common Issues
- Issue Z appears weekly
- Pattern suggests root cause: [analysis]

### Optimization Opportunities
- Task A could be automated
- Skill B could replace manual process
```

### Step 5: Persist Rules

```markdown
## New Rules

### Coding Standards
- [New coding rule 1]
- [New coding rule 2]

### Workflow Rules
- [New workflow rule 1]
- [New workflow rule 2]

### Preferences
- [New preference 1]
- [New preference 2]
```

## Output Format

### Session Summary

```markdown
# Session Wrap-Up Summary

**Date**: 2026-03-04
**Duration**: 2h 30m
**Session ID**: session-123

## Completed Tasks

1. ✅ Security audit of codebase
2. ✅ Code review for PR #45
3. ✅ Test generation for utils.cpp
4. ✅ Documentation updates

## Git Activity

- **Commits**: 3
- **Files Changed**: 12
- **Lines Added**: +156
- **Lines Removed**: -42

## Skills Used

| Skill | Uses | Duration |
|-------|------|----------|
| security-auditor | 2 | 15m |
| code-review | 3 | 25m |
| test-case-generator | 1 | 10m |

## Learnings

- Discovered security vulnerability pattern in X
- Found optimization for Y reducing time by 50%

## Patterns Detected

- Security audits take 2x longer on Mondays
- Test generation works best with clear function signatures

## Rules Added

- Always run security audit before code review
- Use GoogleTest for all new C++ tests

## Next Session Priorities

1. Fix identified security issues
2. Complete PR review feedback
3. Update documentation
```

## Integration

Works with:
- `arc-skill-gitops` - Commit skill changes
- `arc-workflow-orchestrator` - Trigger wrap-up workflow
- `agent-audit` - Include audit metrics in summary

## Configuration

### Wrap-Up Settings

```yaml
wrapup:
  auto_commit: true
  auto_push: true
  extract_learnings: true
  detect_patterns: true
  persist_rules: true
  generate_summary: true
  
commit:
  message_format: "Session work: {summary}"
  include_files: true
  include_metrics: true
  
memory:
  update_daily: true
  update_memory_md: true
  archive_sessions: true
```

## Best Practices

1. **Consistent Timing**: Wrap up at same time daily
2. **Review Before Commit**: Review auto-generated commits
3. **Capture Everything**: Document all learnings
4. **Act on Patterns**: Address detected patterns
5. **Share Summaries**: Share with team if applicable

## Commands

| Command | Description |
|---------|-------------|
| `session-wrap-up` | Manual wrap-up |
| `session-wrap-up --no-commit` | Wrap-up without commit |
| `session-wrap-up --summary-only` | Generate summary only |
| `session-wrap-up configure` | Configure wrap-up settings |
