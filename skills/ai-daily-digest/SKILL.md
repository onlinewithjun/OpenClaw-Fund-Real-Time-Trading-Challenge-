---
name: ai-daily-digest
description: Fetches RSS feeds from 90+ top AI/tech blogs (curated by Karpathy), uses AI to score and filter articles, generates daily digest summaries.
author: royxiao08
version: 1.0.0
---

# AI Daily Digest Skill

## Overview

Automated AI/tech news aggregation and summarization:
- **RSS Aggregation**: Fetch from 90+ curated tech blogs
- **AI Scoring**: Score articles by relevance and importance
- **Smart Filtering**: Filter noise, surface signal
- **Daily Summaries**: Generate concise daily digests
- **Topic Categorization**: Organize by topic areas

## Source Blogs

### AI/ML Blogs

| Blog | RSS Feed |
|------|----------|
| Andrej Karpathy | karpathy.ai |
| OpenAI Blog | openai.com/blog |
| DeepMind | deepmind.com/blog |
| Anthropic | anthropic.com/news |
| Hugging Face | huggingface.co/blog |
| FAIR (Meta) | ai.facebook.com/blog |
| Google AI | ai.googleblog.com |
| NVIDIA DL | developer.nvidia.com/blog |

### Tech News

| Blog | RSS Feed |
|------|----------|
| Hacker News | news.ycombinator.com |
| TechCrunch | techcrunch.com |
| The Verge | theverge.com |
| Ars Technica | arstechnica.com |
| Wired | wired.com |
| MIT Tech Review | technologyreview.com |

### Research

| Blog | RSS Feed |
|------|----------|
| arXiv AI | arxiv.org/list/cs.AI/recent |
| arXiv ML | arxiv.org/list/cs.LG/recent |
| arXiv CV | arxiv.org/list/cs.CV/recent |
| arXiv NLP | arxiv.org/list/cs.CL/recent |

## Usage

### Get Daily Digest

```bash
# Get today's digest
Get AI daily digest

# Get digest for specific date
Get digest for: 2026-03-03

# Get weekly summary
Get weekly AI digest
```

### Filter by Topic

```bash
# AI/ML news only
Get AI/ML digest

# Research papers
Get arXiv digest

# Industry news
Get tech industry digest
```

### Custom Sources

```bash
# Digest from specific sources
Get digest from: Hacker News, TechCrunch

# Exclude sources
Get digest excluding: Twitter, Reddit
```

## Digest Format

### Daily Digest Template

```markdown
# AI Daily Digest - 2026-03-04

## 📰 Top Stories

### 1. [Major AI Breakthrough Announced]
**Source**: OpenAI Blog
**Score**: 9.5/10
**Summary**: OpenAI announces new model with 10x efficiency...
**Link**: https://...

### 2. [New Research Paper on LLMs]
**Source**: arXiv
**Score**: 9.0/10
**Summary**: Researchers propose new attention mechanism...
**Link**: https://...

## 📊 By Category

### AI Research
- Paper: "Efficient Transformers" (arXiv)
- Paper: "Multi-modal Learning" (arXiv)

### Industry News
- Company X raises $100M Series C
- New AI regulation proposed in EU

### Tools & Libraries
- Library Y v2.0 released with major improvements
- New framework for distributed training

## 📈 Trending Topics
1. Efficient AI
2. Multi-modal models
3. AI safety
4. Open source models

## 📅 Events
- Conference X: March 15-17, San Francisco
- Workshop Y: March 20, Online

---
**Total Articles**: 45
**Filtered**: 12 (high relevance)
**Reading Time**: ~15 minutes
```

## Scoring System

### Article Scoring

| Factor | Weight | Description |
|--------|--------|-------------|
| Source Credibility | 25% | Blog reputation, author expertise |
| Recency | 20% | How recent the article is |
| Engagement | 20% | Views, comments, shares |
| Relevance | 20% | Match to user interests |
| Uniqueness | 15% | Novel information vs rehash |

### Score Thresholds

| Score | Action |
|-------|--------|
| 9-10 | Must read (top stories) |
| 7-8 | Recommended (important) |
| 5-6 | Worth scanning |
| <5 | Skip (noise) |

## Processing Pipeline

### Step 1: Fetch

```bash
# Fetch all RSS feeds
Fetch RSS from 90+ sources

# Parse articles
Extract title, summary, link, date
```

### Step 2: Score

```bash
# Calculate scores
Score each article

# Rank articles
Sort by score descending
```

### Step 3: Filter

```bash
# Remove duplicates
Deduplicate similar articles

# Filter low scores
Keep articles >5 score

# Categorize
Group by topic
```

### Step 4: Summarize

```bash
# Generate summaries
AI summarize each article

# Create digest
Compile daily digest
```

## Integration

Works with:
- `agent-daily-planner` - Include digest in morning briefing
- `alex-session-wrap-up` - Add digest to session summary
- `research-cog` - Deep dive into interesting papers

## Configuration

```yaml
daily-digest:
  sources:
    include:
      - hacker-news
      - techcrunch
      - arxiv
    exclude: []
  
  scoring:
    min_score: 5
    top_stories_count: 5
    categories_count: 3
  
  delivery:
    schedule: "0 8 * * *"  # 8 AM daily
    format: markdown
    max_articles: 20
  
  interests:
    - large-language-models
    - computer-vision
    - ai-safety
    - open-source
```

## Best Practices

1. **Morning Reading**: Read digest with morning coffee
2. **Save Interesting**: Bookmark articles for deep reading
3. **Share Highlights**: Share top stories with team
4. **Track Trends**: Monitor trending topics over time

## Commands

| Command | Description |
|---------|-------------|
| `ai-digest` | Get today's digest |
| `ai-digest --date=<date>` | Get digest for date |
| `ai-digest --weekly` | Get weekly summary |
| `ai-digest --topic=<topic>` | Filter by topic |
| `ai-digest --sources=<list>` | Specify sources |
