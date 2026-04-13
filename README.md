# flatten-repo

Dump any git repo into a single labeled text file. Useful for dropping a full codebase into an LLM prompt.

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

- All files tracked by git
- Text files only (binaries skipped)
- Files under 100 KB
- Skips: `node_modules`, `dist`, `build`, `.venv`, etc.

## Requirements

Python 3.9+, git
