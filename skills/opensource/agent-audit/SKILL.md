---
name: agent-audit
description: Audit your AI agent setup for performance, cost, and ROI. Analyze skill usage, token consumption, and efficiency metrics.
author: sharbelayy
version: 1.0.0
---

# Agent Audit Skill

## Overview

Comprehensive AI agent performance and cost audit:
- **Performance Analysis**: Skill execution times, success rates
- **Cost Tracking**: Token usage, API costs, cost per task
- **ROI Analysis**: Value delivered vs. cost incurred
- **Efficiency Metrics**: Optimization opportunities
- **Usage Patterns**: Skill usage frequency, peak times

## Audit Categories

### 1. Performance Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Response Time | Average skill execution time | <5s |
| Success Rate | Successful executions / total | >95% |
| Error Rate | Failed executions / total | <5% |
| Throughput | Executions per hour | Varies |

### 2. Cost Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Token Usage | Total tokens consumed | Monitor |
| Cost per Task | Average cost per task | Optimize |
| Cost per Skill | Cost breakdown by skill | Analyze |
| Monthly Burn | Total monthly cost | Budget |

### 3. Usage Metrics

| Metric | Description | Insight |
|--------|-------------|---------|
| Skill Frequency | Most/least used skills | Optimize stack |
| Peak Hours | Busiest times | Scale planning |
| Task Types | Common task categories | Focus areas |
| Session Length | Average session duration | Engagement |

### 4. ROI Metrics

| Metric | Description | Calculation |
|--------|-------------|-------------|
| Time Saved | Hours saved vs manual | Task time × frequency |
| Cost Avoided | External service costs | Alternative cost - agent cost |
| Quality Improvement | Error reduction | Before vs after error rates |
| Productivity Gain | Output increase | Output per hour change |

## Usage

### Full Audit

```bash
# Complete agent audit
Perform full agent audit

# Audit with ROI analysis
Audit agent with ROI analysis
```

### Targeted Audits

```bash
# Performance audit
Audit agent performance metrics

# Cost audit
Audit agent cost and token usage

# Usage audit
Analyze skill usage patterns
```

### Time-based Audits

```bash
# Last 24 hours
Audit last 24 hours

# Last week
Audit last 7 days

# Last month
Audit last 30 days
```

## Audit Process

### Step 1: Data Collection

- Gather session logs
- Collect token usage data
- Extract skill execution metrics
- Compile cost data

### Step 2: Analysis

- Calculate performance metrics
- Analyze cost patterns
- Identify usage trends
- Compute ROI

### Step 3: Recommendations

- Performance optimizations
- Cost reduction strategies
- Skill stack improvements
- Usage pattern suggestions

## Output Format

### Audit Report

```markdown
# Agent Audit Report

**Period**: 2026-02-04 to 2026-03-04
**Total Sessions**: 156
**Total Cost**: $12.45

## Performance Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg Response Time | 3.2s | <5s | ✅ |
| Success Rate | 97.5% | >95% | ✅ |
| Error Rate | 2.5% | <5% | ✅ |

## Cost Breakdown

| Skill | Tokens | Cost | % of Total |
|-------|--------|------|------------|
| code-review | 50k | $4.50 | 36% |
| security-auditor | 30k | $2.70 | 22% |
| test-case-generator | 25k | $2.25 | 18% |
| Others | 45k | $3.00 | 24% |

## Top Skills by Usage

1. code-review (45 uses)
2. security-auditor (32 uses)
3. test-case-generator (28 uses)

## ROI Analysis

- **Time Saved**: 25 hours/month
- **Cost Avoided**: $500/month (vs external services)
- **Net ROI**: 4000%

## Recommendations

1. **Optimize**: code-review skill uses 36% of tokens
2. **Consider**: Remove unused skills (5 skills never used)
3. **Schedule**: Run heavy tasks during off-peak hours
```

## Optimization Strategies

### Cost Reduction

1. **Skill Optimization**: Use lighter skills when possible
2. **Token Efficiency**: Optimize prompts and context
3. **Caching**: Cache repeated queries
4. **Batch Processing**: Batch similar tasks

### Performance Improvement

1. **Parallel Execution**: Run independent skills concurrently
2. **Skill Selection**: Use most efficient skill for task
3. **Context Management**: Limit context to essentials
4. **Error Reduction**: Improve success rates

## Integration

Works with:
- `arc-workflow-orchestrator` - Optimize workflows
- `arc-skill-gitops` - Remove unused skills
- `alex-session-wrap-up` - Track session metrics

## Best Practices

1. **Regular Audits**: Audit monthly
2. **Track Trends**: Monitor metric trends over time
3. **Set Budgets**: Define cost budgets
4. **Optimize Continuously**: Act on recommendations

## Commands

| Command | Description |
|---------|-------------|
| `agent-audit` | Full agent audit |
| `agent-audit --period=<days>` | Audit specific period |
| `agent-audit --cost` | Cost-focused audit |
| `agent-audit --performance` | Performance audit |
| `agent-audit --roi` | ROI analysis |
