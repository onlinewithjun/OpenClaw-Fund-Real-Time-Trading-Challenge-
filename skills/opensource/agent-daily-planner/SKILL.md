---
name: agent-daily-planner
description: A structured daily planning and execution tracking system for AI agents. Morning planning, task tracking, and end-of-day review.
author: gpunter
version: 1.0.0
---

# Agent Daily Planner

## Overview

Structured daily planning and execution tracking:
- **Morning Planning**: Set daily goals and priorities
- **Task Tracking**: Track tasks throughout the day
- **Time Blocking**: Allocate time for focused work
- **Progress Monitoring**: Track completion throughout day
- **Evening Review**: Reflect on accomplishments and learnings

## Planning Framework

### Morning Planning (9 AM)

| Section | Description | Time |
|---------|-------------|------|
| Today's Goals | 3-5 main objectives | 5 min |
| Priority Tasks | Must-complete tasks | 5 min |
| Time Blocks | Schedule focused work | 5 min |
| Meetings | Scheduled meetings | - |
| Energy Level | Current energy assessment | 1 min |

### Task Categories

| Category | Description | Examples |
|----------|-------------|----------|
| 🔴 Critical | Must do today | Security fixes, deadlines |
| 🟡 Important | Should do today | Code reviews, documentation |
| 🟢 Nice to Have | If time permits | Refactoring, learning |
| 🔵 Delegated | Assigned to others | Team tasks |
| ⚪ Blocked | Waiting on something | Pending reviews |

### Time Blocking

| Block | Time | Focus |
|-------|------|-------|
| Morning Deep Work | 9-12 AM | Complex tasks |
| Afternoon Admin | 1-3 PM | Meetings, emails |
| Afternoon Deep Work | 3-5 PM | Creative tasks |
| Wrap-up | 5-6 PM | Review, planning |

## Usage

### Morning Planning

```bash
# Start morning planning
Plan my day

# Plan with specific goals
Plan day with goals: [goal1, goal2, goal3]

# Review today's plan
Show today's plan
```

### Task Management

```bash
# Add task
Add task: Review PR #45, priority: critical

# Complete task
Complete task: Review PR #45

# Update task status
Update task: Security audit, status: in-progress

# List today's tasks
List today's tasks
```

### Time Tracking

```bash
# Start time block
Start deep work block until 12 PM

# Log time spent
Log 2h on: Code review

# Check time usage
Show time breakdown for today
```

### Evening Review

```bash
# End of day review
Review today

# Generate daily report
Generate daily report

# Plan tomorrow
Plan tomorrow
```

## Daily Plan Format

### Morning Plan Template

```markdown
# Daily Plan - 2026-03-04

## 🎯 Today's Goals
1. Complete security audit of codebase
2. Review and merge 3 PRs
3. Write tests for utils module

## 📋 Priority Tasks

### 🔴 Critical
- [ ] Security audit (est: 2h)
- [ ] PR #45 review (est: 30m)

### 🟡 Important
- [ ] Documentation update (est: 1h)
- [ ] Team standup (est: 15m)

### 🟢 Nice to Have
- [ ] Code refactoring (est: 1h)
- [ ] Read AI papers (est: 30m)

## 📅 Schedule

| Time | Activity | Status |
|------|----------|--------|
| 9-10 AM | Morning planning + email | ✅ |
| 10-12 PM | Deep work: Security audit | 🔄 |
| 12-1 PM | Lunch | ⏳ |
| 1-2 PM | PR reviews | ⏳ |
| 2-3 PM | Team meeting | ⏳ |
| 3-5 PM | Deep work: Tests | ⏳ |
| 5-6 PM | Wrap-up + planning | ⏳ |

## 📝 Notes
- Energy level: 8/10
- Focus: Security and code quality
- Blockers: None
```

### Evening Review Template

```markdown
# Daily Review - 2026-03-04

## ✅ Completed Tasks
- [x] Security audit (2h 15m)
- [x] PR #45 review (25m)
- [x] Documentation update (45m)
- [x] Team standup (15m)

## ❌ Incomplete Tasks
- [ ] Code refactoring → Moved to tomorrow
- [ ] Read AI papers → Moved to tomorrow

## 📊 Time Breakdown

| Category | Planned | Actual | Variance |
|----------|---------|--------|----------|
| Deep Work | 4h | 3h 45m | -15m |
| Meetings | 1h | 1h 15m | +15m |
| Admin | 1h | 45m | -15m |

## 🎯 Goals Progress
- Goal 1: ✅ Complete (security audit done)
- Goal 2: ✅ Complete (3 PRs reviewed)
- Goal 3: ⚠️ Partial (tests 50% done)

## 📈 Energy & Focus
- Morning Energy: 8/10
- Afternoon Energy: 6/10
- Overall Focus: 7/10

## 🧠 Learnings
- Security audit found 2 high-severity issues
- New testing pattern learned for C++

## 📅 Tomorrow's Priorities
1. Complete test coverage
2. Fix security issues
3. Code refactoring
```

## Integration

Works with:
- `ai-daily-digest` - Include in morning briefing
- `alex-session-wrap-up` - Sync with session wrap-up
- `arc-workflow-orchestrator` - Trigger planning workflows

## Configuration

```yaml
daily-planner:
  morning_plan:
    time: "0 9 * * *"  # 9 AM
    include_digest: true
    include_calendar: true
    
  evening_review:
    time: "0 18 * * *"  # 6 PM
    auto_generate: true
    save_to_memory: true
    
  tracking:
    time_tracking: true
    energy_tracking: true
    task_estimation: true
    
  reminders:
    midday_check: true
    wrapup_reminder: true
```

## Best Practices

1. **Plan Morning**: Start each day with clear plan
2. **Time Block**: Protect deep work time
3. **Track Honestly**: Log actual time spent
4. **Review Daily**: Learn from each day
5. **Adjust**: Improve planning based on reviews

## Commands

| Command | Description |
|---------|-------------|
| `plan-day` | Create daily plan |
| `plan-day --goals=<list>` | Plan with specific goals |
| `add-task <task>` | Add new task |
| `complete-task <task>` | Mark task complete |
| `list-tasks` | List today's tasks |
| `review-day` | Evening review |
| `show-stats` | Show productivity stats |

## Productivity Metrics

### Weekly Summary

```markdown
# Weekly Summary - Week 10, 2026

## Task Completion
- Planned: 35 tasks
- Completed: 28 tasks
- Completion Rate: 80%

## Time Allocation
- Deep Work: 18h (45%)
- Meetings: 8h (20%)
- Admin: 6h (15%)
- Other: 8h (20%)

## Goals Achievement
- Weekly Goals: 5
- Achieved: 4
- Rate: 80%

## Energy Trends
- Average Morning: 7.5/10
- Average Afternoon: 6.2/10
- Best Day: Tuesday (8/10)
```
