---
name: arc-workflow-orchestrator
description: Chain skills into automated pipelines with conditional logic, error handling, and audit logging. Workflow orchestration for multi-skill tasks.
author: trypto1019
version: 1.0.0
---

# ARC Workflow Orchestrator

## Overview

Automated workflow orchestration for AI agent skills:
- **Pipeline Creation**: Chain multiple skills into workflows
- **Conditional Logic**: If/else, switch, loops
- **Error Handling**: Try/catch, retry, fallback
- **Audit Logging**: Complete execution history
- **Parallel Execution**: Run skills concurrently

## Workflow Definition

### YAML Workflow

```yaml
# workflow.yaml
name: code-review-pipeline
description: Automated code review and test generation
version: 1.0.0

triggers:
  - event: pr.opened
  - event: manual

steps:
  - id: security-scan
    skill: security-auditor
    action: audit
    params:
      path: "${{ github.workspace }}"
    
  - id: code-review
    skill: code-review
    action: review
    params:
      files: "${{ github.changed_files }}"
    depends_on:
      - security-scan
    condition: "${{ steps.security-scan.output.critical_issues == 0 }}"
    
  - id: generate-tests
    skill: test-case-generator
    action: generate
    params:
      files: "${{ github.changed_files }}"
    depends_on:
      - code-review
      
  - id: simplify-code
    skill: code-simplifier
    action: simplify
    params:
      complexity_threshold: 15
    depends_on:
      - code-review
    condition: "${{ steps.code-review.output.complexity > 15 }}"
    
  - id: post-results
    skill: pr-review
    action: comment
    params:
      summary: "${{ toJSON(steps) }}"
    depends_on:
      - generate-tests
      - simplify-code
```

## Usage

### Create Workflow

```bash
# Create new workflow
Create workflow: code-review-pipeline

# Create from template
Create workflow from template: ci-cd-pipeline
```

### Execute Workflow

```bash
# Run workflow
Execute workflow: code-review-pipeline

# Run with parameters
Execute workflow: code-review-pipeline --params="{\"path\": \"./src\"}"

# Dry run
Execute workflow: code-review-pipeline --dry-run
```

### Manage Workflows

```bash
# List workflows
List all workflows

# View workflow
Show workflow: code-review-pipeline

# Delete workflow
Delete workflow: old-workflow
```

## Workflow Components

### Triggers

| Trigger | Description | Example |
|---------|-------------|---------|
| `manual` | Manual execution | User initiates |
| `schedule` | Cron-based schedule | Daily at 9 AM |
| `event` | Event-based | PR opened, file changed |
| `webhook` | HTTP webhook | External system trigger |

### Actions

| Action | Description | Example |
|--------|-------------|---------|
| `skill` | Execute a skill | Run security-auditor |
| `script` | Run shell script | Execute bash script |
| `http` | HTTP request | Call API endpoint |
| `condition` | Conditional branch | If/else logic |
| `parallel` | Parallel execution | Run multiple steps |

### Conditions

```yaml
# Simple condition
condition: "${{ steps.scan.output.issues == 0 }}"

# Complex condition
condition: "${{ steps.scan.output.critical == 0 && steps.test.output.passed }}"

# Regex condition
condition: "${{ steps.parse.output.type =~ 'security.*' }}"
```

## Error Handling

### Retry Policy

```yaml
steps:
  - id: flaky-step
    skill: some-skill
    retry:
      max_attempts: 3
      delay: 5s
      backoff: exponential
```

### Fallback

```yaml
steps:
  - id: primary
    skill: primary-skill
    fallback:
      - id: backup
        skill: backup-skill
```

### Error Handling

```yaml
steps:
  - id: risky-step
    skill: risky-skill
    on_error:
      - action: notify
        params:
          message: "Step failed"
      - action: rollback
```

## Parallel Execution

```yaml
steps:
  - id: parallel-tests
    parallel:
      - id: unit-tests
        skill: test-runner
        params: { type: "unit" }
      - id: integration-tests
        skill: test-runner
        params: { type: "integration" }
      - id: security-scan
        skill: security-auditor
```

## Audit Logging

### Execution Log

```yaml
execution:
  id: exec-123
  workflow: code-review-pipeline
  started_at: 2026-03-04T11:30:00Z
  status: running
  steps:
    - id: security-scan
      status: completed
      duration: 5s
      output: { issues: 0 }
    - id: code-review
      status: running
      started_at: 2026-03-04T11:30:05Z
```

### Output Variables

```yaml
outputs:
  review_summary: "${{ steps.code-review.output.summary }}"
  test_coverage: "${{ steps.generate-tests.output.coverage }}"
  security_status: "${{ steps.security-scan.output.status }}"
```

## Integration

Works with:
- `arc-skill-gitops` - Deploy workflows via GitOps
- `arc-security-audit` - Audit workflow security
- `alex-session-wrap-up` - Log workflow completions

## Best Practices

1. **Modular Design**: Small, focused workflows
2. **Error Handling**: Always handle failures
3. **Logging**: Log all executions
4. **Testing**: Test workflows before production
5. **Documentation**: Document workflow purpose

## Commands

| Command | Description |
|---------|-------------|
| `workflow create <name>` | Create new workflow |
| `workflow execute <name>` | Execute workflow |
| `workflow list` | List all workflows |
| `workflow status <id>` | Check execution status |
| `workflow logs <id>` | View execution logs |

## Example Workflows

### CI/CD Pipeline

```yaml
name: ci-cd
steps:
  - id: lint
    skill: code-review
  - id: test
    skill: test-case-generator
  - id: security
    skill: security-auditor
  - id: build
    skill: build-skill
  - id: deploy
    skill: deploy-skill
```

### Daily Report

```yaml
name: daily-report
trigger: schedule (9 AM daily)
steps:
  - id: gather-news
    skill: ai-daily-digest
  - id: check-calendar
    skill: calendar-skill
  - id: generate-report
    skill: reporter-skill
  - id: send-report
    skill: email-skill
```
