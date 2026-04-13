#!/usr/bin/env python3
"""
flatten-repo: Dump any git repo into a single labeled text file.
Great for feeding codebases into LLMs.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

BINARY_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.webp', '.bmp',
    '.mp3', '.mp4', '.wav', '.avi', '.mov', '.webm',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.zip', '.tar', '.gz', '.rar', '.7z',
    '.exe', '.dll', '.so', '.dylib', '.bin',
    '.pyc', '.pyo', '.class', '.o',
    '.woff', '.woff2', '.ttf', '.eot', '.otf',
    '.sqlite', '.db', '.pkl', '.lock', '.lockb',
}

SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', '.venv', 'venv',
    'dist', 'build', '.next', '.cache', 'coverage',
    '.idea', '.vscode', 'target', 'vendor',
}

MAX_FILE_BYTES = 100 * 1024  # skip files over 100KB


def is_binary(path: Path) -> bool:
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    try:
        with open(path, 'rb') as f:
            return b'\x00' in f.read(1024)
    except:
        return True


def git_tracked_files(repo: Path) -> list[Path]:
    try:
        out = subprocess.run(
            ['git', 'ls-files'],
            cwd=repo, capture_output=True, text=True, check=True
        ).stdout.strip()
        return sorted(
            repo / line for line in out.splitlines()
            if line and (repo / line).is_file()
        )
    except subprocess.CalledProcessError:
        print("Error: not a git repository (or git is not installed).")
        sys.exit(1)


def clone(url: str, dest: Path):
    print(f"Cloning {url}...")
    try:
        subprocess.run(
            ['git', 'clone', '--depth', '1', url, str(dest)],
            check=True, capture_output=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Clone failed: {e.stderr.decode()}")
        sys.exit(1)


def flatten(repo: Path, out_path: str = None) -> str:
    files = git_tracked_files(repo)
    out_path = out_path or f"{repo.name}.txt"

    included, skipped = 0, 0
    lines = [
        f"# {repo.name}",
        f"# {len(files)} tracked files",
        "=" * 72, ""
    ]

    for f in files:
        rel = f.relative_to(repo)

        if any(part in SKIP_DIRS for part in rel.parts):
            skipped += 1
            continue
        if is_binary(f) or f.stat().st_size > MAX_FILE_BYTES:
            skipped += 1
            continue

        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
        except:
            skipped += 1
            continue

        lines += [f"{'='*72}", f"FILE: {rel}", f"{'='*72}", content, ""]
        included += 1

    lines += [f"{'='*72}", f"# {included} files included, {skipped} skipped"]

    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))

    return out_path, included, skipped


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    out_arg = sys.argv[2] if len(sys.argv) > 2 else None

    if target.startswith(('http://', 'https://', 'git@')):
        tmp = tempfile.mkdtemp()
        repo = Path(tmp) / 'repo'
        clone(target, repo)
        try:
            out, n, s = flatten(repo, out_arg)
        finally:
            shutil.rmtree(tmp)
    else:
        repo = Path(target).resolve()
        if not repo.exists():
            print(f"Error: {repo} does not exist.")
            sys.exit(1)
        out, n, s = flatten(repo, out_arg)

    print(f"✓  Written to {out}  ({n} files, {s} skipped)")


if __name__ == '__main__':
    main()
