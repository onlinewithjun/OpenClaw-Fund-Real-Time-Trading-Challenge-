# Memory Maintenance Schedule

## Daily Tasks (Automated via Heartbeat)
- [x] Review today's memory file for redundant system status sections
- [x] Remove verbose system status outputs that can be retrieved on-demand
- [x] Keep only essential decision points, user preferences, and unique insights

## Weekly Tasks (Manual or Semi-Automated)
- [x] Archive memory files older than 7 days to `memory/archive/`
- [x] Update MEMORY.md with distilled learnings from the week
- [x] Clean up outdated information from MEMORY.md
- [x] Verify qmd search index is up-to-date

## Monthly Tasks
- [x] Review and prune MEMORY.md for relevance
- [x] Analyze memory usage patterns and adjust strategies
- [x] Update memory optimization guide based on lessons learned

## Aggressive Compaction Rules
1. **System Status Sections**: Remove entire "## 系统状态" sections - these can be regenerated
2. **File Size Limit**: Keep daily memory files under 2KB when possible
3. **Redundant Information**: Remove duplicate explanations or repetitive content
4. **Temporary Context**: Remove context that's only relevant for immediate session

## Token-Saving Strategies
- Use bullet points instead of paragraphs when possible
- Reference external files instead of embedding large content
- Use concise language while preserving meaning
- Prioritize actionable insights over verbose descriptions

## Efficient Retrieval Configuration
- Leverage existing qmd search system for semantic retrieval
- Maintain clean, well-structured memory files for better indexing
- Use consistent headings and formatting for better parsing
- Regular index updates after significant memory changes