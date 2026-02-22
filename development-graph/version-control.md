---
description: "Лучшие практики Git и контроля версий"
version: "1.0.0"
tags: ["git", "version-control", "workflow"]
related: ["code-review", "refactoring", "clean-code"]
---

# Version Control

## Overview

Version control is your safety net. It tracks every change, lets you undo mistakes, and enables collaboration. Good version control practices prevent disasters and make team work possible. Git is the tool, but version control is the practice.

## Core Principles

### 1. Commit Often, Commit Small

**Bad:**
```bash
# One commit for everything
git add .
git commit -m "Fixed everything"
```

**Good:**
```bash
# Commits for logical units of work
git add user_service.py
git commit -m "Add user validation"

git add email_service.py
git commit -m "Implement email notifications"

git add tests/
git commit -m "Add tests for user creation"
```

**Benefits:**
- Easier to understand history
- Easier to revert changes
- Easier to review

### 2. Write Meaningful Commit Messages

**Bad:**
```bash
git commit -m "update"
git commit -m "fix bug"
git commit -m "wip"
```

**Good:**
```bash
git commit -m "Add user email validation"
git commit -m "Fix crash when user ID is null"
git commit -m "Implement checkout flow"
```

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change without functional change
- `docs`: Documentation change
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

**Example:**
```
feat(auth): add JWT token generation

Implements secure token generation with expiration.

Closes #123
```

### 3. Branching Strategy

**Feature Branch Workflow:**
```
main
  │
  ├── feature/user-authentication
  │    ├── Implement login
  │    ├── Add tests
  │    └── Merge back to main
  │
  ├── feature/payment-processing
  └── feature/email-notifications
```

**Rules:**
- Never commit directly to main
- One feature per branch
- Delete branch after merge

## Common Git Workflows

### 1. Feature Workflow

```bash
# Create feature branch
git checkout -b feature/add-user-auth

# Make changes
# ... write code ...

# Stage and commit
git add .
git commit -m "feat(auth): add user authentication"

# Push to remote
git push origin feature/add-user-auth

# Create pull request
# Code review happens here

# Merge to main after review
git checkout main
git merge feature/add-user-auth
git branch -d feature/add-user-auth
```

### 2. Bug Fix Workflow

```bash
# Create fix branch from main
git checkout main
git checkout -b fix/login-crash

# Fix the bug
# ... write fix ...

# Test thoroughly
python -m pytest tests/

# Commit with clear message
git commit -m "fix(auth): handle null user ID in login"

# Push and create PR
git push origin fix/login-crash
```

### 3. Hotfix Workflow

```bash
# Create hotfix branch from production
git checkout production
git checkout -b hotfix/critical-bug

# Quick fix
# ... minimal changes ...

# Commit and merge
git commit -m "fix: critical bug in production"
git checkout production
git merge hotfix/critical-bug
git checkout main
git merge hotfix/critical-bug

# Tag release
git tag v1.0.1
```

## Git Commands Reference

### Daily Commands

```bash
# Check status
git status

# Stage files
git add file.py
git add .

# Commit changes
git commit -m "feat: add new feature"

# View history
git log --oneline --graph

# Pull latest changes
git pull origin main

# Push changes
git push origin feature-branch
```

### Branch Management

```bash
# Create branch
git checkout -b new-feature

# List branches
git branch -a

# Delete local branch
git branch -d feature-branch

# Delete remote branch
git push origin --delete feature-branch

# Rename branch
git branch -m old-name new-name
```

### Undoing Mistakes

```bash
# Unstage file
git reset HEAD file.py

# Discard local changes
git checkout -- file.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert specific commit
git revert abc123
```

### Advanced

```bash
# Interactive rebase
git rebase -i HEAD~3

# Cherry-pick commit
git cherry-pick abc123

# Stash changes
git stash
git stash pop

# View differences
git diff
git diff main
git diff HEAD~1
```

## Common Mistakes

### 1. Committing Too Much

**Bad:** One commit for a week's work
**Good:** Multiple small commits for logical changes

**Why:** Easier to review, revert, and understand.

### 2. Committing Temporary Files

**Bad:** Committing `.pyc`, `node_modules`, `.env`
**Good:** Using `.gitignore`

```bash
# .gitignore
*.pyc
node_modules/
.env
__pycache__/
```

### 3. Not Pulling Before Pushing

**Bad:** Pushing without pulling first
**Good:** Always pull, resolve conflicts, then push

**Why:** Avoids merge conflicts.

### 4. Committing Broken Code

**Bad:** Code doesn't run, commit anyway
**Good:** Ensure tests pass before committing

**Rule:** Don't commit if tests fail.

## Integration

Version control connects to:
- [[code-review]] — PRs are code review
- [[refactoring]] — Small commits enable safe refactoring
- [[clean-code]] — Commits should be logical units
- [[debugging]] — `git bisect` helps debug

## Quick Reference

| Command | Purpose |
|----------|---------|
| `git status` | Show working directory status |
| `git add` | Stage changes |
| `git commit` | Save changes |
| `git push` | Send to remote |
| `git pull` | Get from remote |
| `git checkout -b` | Create branch |
| `git merge` | Merge branch |
| `git log` | View history |

## Best Practices

### 1. Use Pull Requests

Never push directly to main:
- Create feature branch
- Make changes
- Open pull request
- Get [[code-review]]
- Merge after approval

### 2. Keep History Clean

Use rebase for local branches:
```bash
git rebase main  # Rebase onto main
```

Use merge for integrating to main:
```bash
git checkout main
git merge feature-branch  # Merge, don't rebase
```

### 3. Write Good Commit Messages

Follow format:
```
type(scope): subject

body

footer
```

Be specific, not vague.

### 4. Test Before Committing

```bash
# Run tests
python -m pytest tests/

# Run linter
flake8 .

# Then commit
git commit -m "feat: add new feature"
```

## Debugging with Git

### Git Bisect

Find when bug was introduced:
```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark known good commit
git bisect good abc123

# Git will check out middle commit
# Test, then tell Git:
git bisect good  # or bad

# Repeat until found
git bisect reset
```

### Git Blame

Find who changed a line:
```bash
git blame file.py
```

Shows commit and author for each line.

## Workflow Examples

### Daily Workflow

```bash
# Morning: Pull latest
git pull origin main

# Work on feature
git checkout -b feature/new-stuff
# ... code ...
git commit -m "feat: implement feature"

# Afternoon: Push for review
git push origin feature/new-stuff
# Create PR

# Next morning: Review feedback
# ... fix issues ...
git commit -m "fix: address review comments"
git push
```

### Release Workflow

```bash
# Create release branch
git checkout main
git checkout -b release/v1.2.0

# Update version, changelog
# ... ...

# Tag release
git tag v1.2.0
git push origin v1.2.0

# Deploy
# ... deployment ...

# Merge back to main
git checkout main
git merge release/v1.2.0
```

## Wisdom

> "If it's not in Git, it doesn't exist."

Commit often.
Write clear messages.
Use branches.

Version control is your undo button for code.
Use it.
