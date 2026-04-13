# flatten-repo

Flatten any git repo into a single text file. Paste into ChatGPT/Claude for instant full-codebase context — no agents, no token waste.

## Why?

AI coding agents (Cursor, Copilot, etc.) spend tokens *exploring* your repo — reading files one by one, searching, inferring structure. Every tool call costs money. And they start from scratch each conversation.

**flatten-repo skips all of that.** One command → one text file with your entire codebase, labeled and ready. Paste it into ChatGPT's free tier and ask anything — it has full context instantly.

Think of it this way: an agent reads a repo like someone wandering a new city. `flatten-repo` hands it the complete map upfront.

## Usage

```bash
# current directory
python flatten_repo.py

# local repo
python flatten_repo.py /path/to/repo

# GitHub URL (auto-clones)
python flatten_repo.py https://github.com/user/repo

# custom output filename
python flatten_repo.py https://github.com/user/repo out.txt
```

Output is written to `<repo-name>.txt` by default.

## Install as a command

```bash
chmod +x flatten_repo.py
sudo ln -s $(pwd)/flatten_repo.py /usr/local/bin/flatten-repo

# then just:
flatten-repo https://github.com/user/repo
```

## What gets included

- All git-tracked files
- Text/code files only (binaries auto-skipped)
- Files under 100 KB
- Auto-skips: `node_modules`, `dist`, `build`, `.venv`, `__pycache__`, etc.

## Output format

```
========================================================================
FILE: src/index.ts
========================================================================
import { App } from './App';
...

========================================================================
FILE: src/utils/helpers.py
========================================================================
def process(data):
...
```

## Requirements

Python 3.9+, git
