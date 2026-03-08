---
name: active-maintenance
description: Automated system health and memory metabolism for OpenClaw. Monitors system state, cleans up resources, and maintains optimal performance.
author: xiaowenzhou
version: 1.0.0
---

# Active Maintenance Skill

## Overview

Automated OpenClaw system maintenance:
- **Health Monitoring**: System resource monitoring
- **Memory Management**: Memory file cleanup and compaction
- **Session Cleanup**: Archive old sessions
- **Resource Optimization**: Free disk space, clean temp files
- **Performance Tuning**: Optimize configuration

## Maintenance Tasks

### 1. Health Checks

| Check | Description | Frequency |
|-------|-------------|-----------|
| Disk Space | Check available disk space | Hourly |
| Memory Usage | Monitor memory consumption | Hourly |
| Session Count | Count active sessions | Daily |
| Log Size | Check log file sizes | Daily |
| Skill Health | Verify skill functionality | Weekly |

### 2. Memory Management

| Task | Description | Frequency |
|------|-------------|-----------|
| Compact Daily Files | Compress old daily memory files | Daily |
| Archive Old Memory | Move old files to archive | Weekly |
| Clean Temp Memory | Remove temp memory files | Daily |
| Optimize MEMORY.md | Compact long-term memory | Weekly |

### 3. Session Management

| Task | Description | Frequency |
|------|-------------|-----------|
| Archive Sessions | Archive sessions >7 days | Daily |
| Clean Failed Sessions | Remove failed session data | Daily |
| Limit Active Sessions | Cap active session count | As needed |

### 4. Resource Cleanup

| Task | Description | Frequency |
|------|-------------|-----------|
| Clean Temp Files | Remove temp files | Daily |
| Clean Logs | Rotate and compress logs | Weekly |
| Clean Cache | Clear skill cache | Weekly |
| Clean Downloads | Remove old downloads | Monthly |

## Usage

### Manual Maintenance

```bash
# Run full maintenance
Run system maintenance

# Run specific task
Run memory compaction

# Run health check
Check system health
```

### Scheduled Maintenance

```bash
# Enable auto-maintenance
Enable automatic maintenance

# Set schedule
Schedule maintenance: daily at 03:00
```

## Maintenance Process

### Step 1: Health Assessment

```bash
# Check disk space
df -h

# Check memory
free -m

# Check session count
Count sessions

# Check log sizes
du -sh logs/*
```

### Step 2: Execute Tasks

```bash
# Compact memory files
Compact daily memory

# Archive old sessions
Archive sessions older than 7 days

# Clean temp files
Clean temporary files

# Rotate logs
Rotate log files
```

### Step 3: Generate Report

```markdown
# Maintenance Report

**Date**: 2026-03-04
**Duration**: 2m 15s

## Health Status

| Component | Status | Details |
|-----------|--------|---------|
| Disk Space | ✅ | 150GB free (75%) |
| Memory | ✅ | 4GB used (50%) |
| Sessions | ✅ | 12 active |
| Logs | ⚠️ | 500MB (needs rotation) |

## Actions Taken

1. ✅ Compacted 5 daily memory files (saved 2MB)
2. ✅ Archived 10 old sessions
3. ✅ Cleaned 50 temp files (saved 100MB)
4. ✅ Rotated log files
5. ⚠️ Warning: Skill cache growing (500MB)

## Recommendations

1. Consider increasing session archive threshold
2. Review skill cache retention policy
```

## Integration

Works with:
- `alex-session-wrap-up` - Trigger after session wrap-up
- `arc-skill-gitops` - Commit maintenance changes
- `agent-audit` - Include maintenance metrics

## Configuration

```yaml
maintenance:
  auto_enabled: true
  schedule: "0 3 * * *"  # Daily at 3 AM
  
  disk:
    warn_threshold: 90%
    critical_threshold: 95%
    clean_temp: true
    
  memory:
    compact_daily: true
    archive_after_days: 7
    optimize_memory_md: true
    
  sessions:
    archive_after_days: 7
    max_active: 50
    clean_failed: true
    
  logs:
    rotate_size: 100MB
    keep_count: 5
    compress: true
```

## Best Practices

1. **Schedule Off-Peak**: Run maintenance during low-usage hours
2. **Monitor Alerts**: Set up alerts for critical thresholds
3. **Review Reports**: Review maintenance reports weekly
4. **Adjust Thresholds**: Tune thresholds based on usage patterns

## Commands

| Command | Description |
|---------|-------------|
| `maintenance run` | Run full maintenance |
| `maintenance health` | Check system health |
| `maintenance compact` | Compact memory files |
| `maintenance archive` | Archive old data |
| `maintenance clean` | Clean temp files |
| `maintenance configure` | Configure settings |
