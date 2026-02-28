---
title: repository.sh
description: Manage module repositories for the TAPPaaS platform
---

# repository.sh

Manages module repositories for the TAPPaaS platform. Supports adding, removing, modifying, and listing external module repositories alongside the main TAPPaaS repository.

## Usage

```bash
repository.sh <command> [options]
```

## Commands

| Command | Description |
|---------|-------------|
| `add <url> [--branch <branch>]` | Add a new module repository |
| `remove <name> [--force]` | Remove a module repository |
| `modify <name> [--url <url>] [--branch <branch>]` | Modify a repository |
| `list` | List all tracked repositories |

## Examples

```bash
# Add a community module repository
repository.sh add github.com/someone/tappaas-community

# Add with a specific branch
repository.sh add github.com/someone/tappaas-community --branch develop

# List all repositories
repository.sh list

# Switch a repository to a different branch
repository.sh modify tappaas-community --branch stable

# Change a repository's URL
repository.sh modify tappaas-community --url github.com/other/repo --branch main

# Remove a repository
repository.sh remove tappaas-community

# Force remove even if modules are installed from it
repository.sh remove tappaas-community --force
```

## What `add` does

1. Validates the repository URL is reachable via `git ls-remote`
2. Clones the repository to `/home/tappaas/<name>/`
3. Checks out the specified branch (default: `main`)
4. Verifies the repo contains `src/modules.json`
5. Warns on VMID or module name conflicts with existing repos
6. Updates `configuration.json` with the new repository entry

## What `remove` does

1. Checks that no installed modules have their `location` pointing into the repository
2. Removes the repository directory
3. Updates `configuration.json` to remove the repository entry

## What `modify` does

- **Branch-only change**: Fetches and checks out the new branch in place
- **URL change**: Validates new repo has all currently-installed modules, re-clones, and updates module `location` fields

## Notes

- Repository URLs use the same format as `upstreamGit` (without `https://` prefix)
- The main TAPPaaS repository is the first entry in the `repositories` array
- All repositories are treated equally — no special handling for the main repo
- VMID and module name conflicts are warnings, not errors

## See Also

- [Git Structure](../../architecture/cicd-design/git-structure.md) - Repository organization and GitOps workflow
