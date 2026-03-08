---
name: 2nd-brain
description: Personal knowledge base for capturing and retrieving information about people, places, restaurants, games, tech. Second brain for AI agents.
author: coderaven
version: 1.0.0
---

# 2nd Brain Skill

## Overview

Personal knowledge base for AI agents:
- **Knowledge Capture**: Store information about people, places, things
- **Smart Retrieval**: Quick lookup with semantic search
- **Relationship Mapping**: Connect related information
- **Context Awareness**: Provide relevant context during conversations
- **Memory Augmentation**: Extend agent's memory capabilities

## Knowledge Categories

### People

| Field | Description |
|-------|-------------|
| Name | Person's name |
| Role | Job title / relationship |
| Contact | Email, phone, social |
| Notes | Personal notes, preferences |
| Last Interaction | Date and context |

### Places

| Field | Description |
|-------|-------------|
| Name | Place name |
| Type | Restaurant, office, home, etc. |
| Location | Address, coordinates |
| Notes | Reviews, preferences, tips |
| Visits | Visit history |

### Technology

| Field | Description |
|-------|-------------|
| Name | Technology name |
| Category | Language, framework, tool |
| Version | Current version |
| Usage | How/when used |
| Notes | Tips, gotchas, resources |

### Projects

| Field | Description |
|-------|-------------|
| Name | Project name |
| Status | Active, completed, on hold |
| Goal | Project objective |
| Notes | Key decisions, learnings |
| Links | Related files, repos |

## Usage

### Capture Information

```bash
# Add person
Remember: John is a C++ developer at Company X, prefers morning meetings

# Add place
Remember: Favorite lunch spot is Noodle House on Main St, order #7

# Add technology
Remember: Using Qt 6.5 for UI framework, avoid deprecated widgets

# Add project
Remember: Project Phoenix - migrating legacy C++ code to modern standards
```

### Retrieve Information

```bash
# Find person
What do I know about John?

# Find place
Where did I eat last week?

# Find technology
What version of Qt are we using?

# Find project
Status of Project Phoenix?
```

### Search Knowledge

```bash
# Semantic search
Search for: C++ developers

# Filter by category
Find all restaurants

# Find by date
What did I learn last week?
```

## Knowledge Format

### Entry Format

```markdown
---
type: person
name: John Smith
role: Senior C++ Developer
company: Tech Corp
contact: john@techcorp.com
tags: [cpp, backend, mentor]
---

## Notes
- Prefers morning meetings (9-11 AM)
- Expert in OpenHarmony N-API
- Mentoring junior developers

## Interactions
- 2026-03-01: Discussed code review process
- 2026-02-15: Code review session
```

### Relationship Mapping

```markdown
## Relationships
- Works with: Jane Doe (frontend)
- Reports to: Bob Wilson (manager)
- Collaborates with: Team Alpha
```

## Integration

Works with:
- `MEMORY.md` - Sync important knowledge
- `alex-session-wrap-up` - Capture session learnings
- `agent-daily-planner` - Add context to planning

## Best Practices

1. **Capture Immediately**: Add info when learned
2. **Tag Consistently**: Use consistent tagging
3. **Review Regularly**: Review and update entries
4. **Link Related**: Connect related entries
5. **Prune Old**: Archive outdated information

## Commands

| Command | Description |
|---------|-------------|
| `2nd-brain add <info>` | Add new knowledge |
| `2nd-brain find <query>` | Search knowledge |
| `2nd-brain list [category]` | List entries |
| `2nd-brain update <entry>` | Update entry |
| `2nd-brain delete <entry>` | Delete entry |
| `2nd-brain export` | Export knowledge base |
