---
name: bat-cat
description: A cat clone with syntax highlighting, line numbers, and Git integration. Enhanced file viewing for developers.
author: arnarsson
version: 1.0.0
---

# Bat Cat Skill

## Overview

Enhanced `cat` command with developer-friendly features:
- **Syntax Highlighting**: Auto-detect and highlight code
- **Line Numbers**: Display line numbers for reference
- **Git Integration**: Show Git diff markers
- **Pagination**: Automatic paging for long files
- **Search**: In-file search capabilities

## Features

### Syntax Highlighting

| Language | Support |
|----------|---------|
| C/C++ | ✅ Full |
| Python | ✅ Full |
| JavaScript/TypeScript | ✅ Full |
| Java | ✅ Full |
| Go | ✅ Full |
| Rust | ✅ Full |
| Markdown | ✅ Full |
| JSON/YAML | ✅ Full |
| Shell | ✅ Full |
| HTML/CSS | ✅ Full |

### Line Numbering

- Continuous numbering
- Critical line highlighting
- Range selection

### Git Integration

- Show modified lines
- Display added/removed markers
- Compare with HEAD

## Usage

### View Files

```bash
# Basic file view
View file: src/utils.cpp

# With line numbers
View file with line numbers: config.yaml

# With syntax highlighting
View with highlighting: main.py
```

### View Ranges

```bash
# Specific lines
View lines 1-50 of: large_file.cpp

# Around specific line
View around line 100 of: utils.ts
```

### Git Integration

```bash
# Show Git changes
View with Git diff: modified_file.cpp

# Compare with HEAD
Compare with HEAD: config.json
```

### Search

```bash
# Search in file
Search for "function" in: utils.cpp

# Search with context
Search "error" with 5 lines context: log.txt
```

## Output Format

### Standard View

```
     1 │ #include <iostream>
     2 │ #include <vector>
     3 │ 
     4 │ int main() {
     5 │     std::vector<int> numbers = {1, 2, 3};
     6 │     for (int num : numbers) {
     7 │         std::cout << num << std::endl;
     8 │     }
     9 │     return 0;
    10 │ }
```

### Git Diff View

```
     1 │ #include <iostream>
     2 │ #include <vector>
   3 + │ #include <algorithm>
     4 │ 
     5 │ int main() {
     6 │     std::vector<int> numbers = {1, 2, 3, 4, 5};
   7 + │     std::sort(numbers.begin(), numbers.end());
     8 │     for (int num : numbers) {
     9 │         std::cout << num << std::endl;
    10 │     }
    11 │     return 0;
    12 │ }
```

### Search Results

```
File: utils.cpp
Line 45: void handleError(const std::string& error) {
Line 46:     std::cerr << "Error: " << error << std::endl;
Line 47: }

File: main.cpp  
Line 12:     handleError("Initialization failed");
```

## Integration

Works with:
- `code-review` - View code during review
- `code-simplifier` - View before/after simplification
- `security-auditor` - View vulnerable code sections

## Best Practices

1. **Use Line Numbers**: Reference specific lines in discussions
2. **Enable Git Diff**: Always show changes when reviewing
3. **Syntax Highlighting**: Use for all code files
4. **Pagination**: Enable for files >50 lines

## Commands

| Command | Description |
|---------|-------------|
| `bat view <file>` | View file with highlighting |
| `bat view <file> --lines <start>-<end>` | View line range |
| `bat view <file> --git` | Show Git diff |
| `bat search <pattern> <file>` | Search in file |
| `bat compare <file1> <file2>` | Compare two files |

## Configuration

```yaml
bat:
  theme: GitHub
  line_numbers: true
  git_integration: true
  paging: auto
  wrap: false
  tabs: 4
```
