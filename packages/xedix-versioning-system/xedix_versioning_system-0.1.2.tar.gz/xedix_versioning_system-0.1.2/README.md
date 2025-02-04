# XediX Versioning System

A lightweight version control system implemented in Python.

## Installation

```bash
pip install xedix-versioning-system
```

## Usage

After installation, you can use the `xvs` command:

```bash
xvs branch main                            # Switch to or create 'main' branch
xvs commit "file1.txt" "Initial commit"    # Commit changes
xvs stage "file1.txt" "Work in progress"   # Stage changes
xvs init
xvs status
```