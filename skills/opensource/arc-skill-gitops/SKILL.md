---
name: arc-skill-gitops
description: Automated deployment, rollback, and version management for agent workflows and skills. GitOps-style skill lifecycle management.
author: trypto1019
version: 1.0.0
---

# ARC Skill GitOps

## Overview

GitOps-style skill lifecycle management:
- **Version Control**: Track skill versions with Git
- **Automated Deployment**: Deploy skills from Git commits
- **Rollback Support**: Rollback to previous versions
- **State Management**: Maintain skill state in Git
- **Audit Trail**: Complete change history

## Core Concepts

### GitOps Principles

1. **Declarative**: Skills defined in Git manifests
2. **Versioned**: Every change tracked in Git
3. **Automated**: Changes applied automatically
4. **Auditable**: Full history of changes

### Skill Manifest

```yaml
# skills.yaml
skills:
  - name: code-review
    version: 1.0.0
    source: workspace/skills/code-review
    enabled: true
    config:
      autoReview: true
      
  - name: security-auditor
    version: 1.0.0
    source: workspace/skills/security-auditor
    enabled: true
```

## Usage

### Deploy Skills

```bash
# Deploy all skills from manifest
Deploy skills from git

# Deploy specific skill
Deploy skill: code-review version 1.0.0

# Deploy from branch
Deploy skills from branch: feature/new-skills
```

### Rollback

```bash
# Rollback to previous version
Rollback skill: code-review

# Rollback to specific commit
Rollback to commit: abc123

# Rollback all skills
Rollback all skills to last stable
```

### Version Management

```bash
# List skill versions
List versions of: code-review

# Update skill version
Update code-review to version 1.1.0

# Check for updates
Check for skill updates
```

## GitOps Workflow

### Step 1: Initialize

```bash
# Initialize GitOps repository
arc-gitops init

# Create initial manifest
arc-gitops create-manifest
```

### Step 2: Make Changes

```bash
# Add new skill
arc-gitops add skill-name --version=1.0.0

# Update skill
arc-gitops update skill-name --version=1.1.0

# Remove skill
arc-gitops remove skill-name
```

### Step 3: Commit & Deploy

```bash
# Commit changes
arc-gitops commit -m "Add code-review skill"

# Deploy changes
arc-gitops apply
```

### Step 4: Verify

```bash
# Check deployment status
arc-gitops status

# Verify skills
arc-gitops verify
```

## Rollback Strategies

### Strategy 1: Last Known Good

```bash
# Rollback to last stable state
arc-gitops rollback --strategy=last-stable
```

### Strategy 2: Specific Commit

```bash
# Rollback to specific commit
arc-gitops rollback --commit=abc123
```

### Strategy 3: Time-based

```bash
# Rollback to state from 24 hours ago
arc-gitops rollback --time="24h ago"
```

## State Management

### State File

```yaml
# .arc/state.yaml
currentState:
  deployedAt: 2026-03-04T11:30:00Z
  commit: abc123def
  skills:
    code-review:
      version: 1.0.0
      status: deployed
      health: healthy
    security-auditor:
      version: 1.0.0
      status: deployed
      health: healthy
```

### Health Checks

```bash
# Check skill health
arc-gitops health

# Check specific skill
arc-gitops health code-review
```

## Integration

Works with:
- `arc-security-audit` - Audit skills before deploy
- `arc-workflow-orchestrator` - Chain deployments
- `alex-session-wrap-up` - Commit session changes

## Best Practices

1. **Commit Often**: Small, frequent commits
2. **Review Changes**: Review before applying
3. **Test First**: Test in staging before production
4. **Monitor Health**: Continuous health monitoring
5. **Document Changes**: Clear commit messages

## Commands

| Command | Description |
|---------|-------------|
| `arc-gitops init` | Initialize GitOps repository |
| `arc-gitops apply` | Apply pending changes |
| `arc-gitops rollback` | Rollback to previous state |
| `arc-gitops status` | Show current status |
| `arc-gitops health` | Check skill health |
| `arc-gitops history` | Show change history |

## Example Workflow

```bash
# Initialize
arc-gitops init

# Add skills
arc-gitops add code-review
arc-gitops add security-auditor
arc-gitops add test-case-generator

# Commit
arc-gitops commit -m "Add core development skills"

# Deploy
arc-gitops apply

# Verify
arc-gitops status
arc-gitops health
```
