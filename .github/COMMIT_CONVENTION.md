# Commit Convention for TRMNL Dashboard

## Author Policy

**All commits MUST be authored by Michael Muyakwa (mmuyakwa)**
- Name: `Michael Muyakwa`  
- Email: `34812005+mmuyakwa@users.noreply.github.com`

## Commit Message Format

```
<type>: <subject>

<body>

Author: Michael Muyakwa (mmuyakwa)
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting, missing semicolons, etc
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `deps`: Dependency updates

### Examples

```bash
feat: add fullscreen image viewer with zoom controls

Implemented interactive fullscreen mode for TRMNL display images
with click-to-zoom, keyboard shortcuts, and auto-hide UI.

Author: Michael Muyakwa (mmuyakwa)
```

```bash
deps: update Flask to v3.1.0

Updated Flask framework to latest stable version with security patches.

Author: Michael Muyakwa (mmuyakwa)
```

## Automated Enforcement

Git hooks are configured to:
- ✅ Set correct author information automatically
- ✅ Remove any AI assistant references from commit messages
- ✅ Ensure all commits are attributed to mmuyakwa
- ✅ Clean up commit message formatting

## Manual Override Prevention

The repository is configured to prevent commits from other authors:
- Global Git config set to mmuyakwa
- Local Git config enforced
- Pre-commit hooks validate authorship
- Commit message templates ensure proper attribution