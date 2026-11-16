# dspygen migration plan v26.11.16

Standing: UNVERIFIED

## Identity
- Path: /Users/sac/dev/dspygen
- Remote: https://github.com/seanchatmangpt/dspygen.git
- Branch: main@5827495 (upstream origin/main)
- Last commit: 2026-09-26 (dependabot merges); commits: 295; size: 1631 MB
- Languages/build: Python (pyproject.toml, poetry.lock), Makefile, Docker, ggen.toml
- Nested repos: none

## Observed state
- Dirty: 0; untracked: 0; ahead/behind: 0/0; stash: 0
- Unpushed local branches (1): modep/preserve-20260926T1256Z-dspygen (a "preserve: dirty
  worktree snapshot" branch — intentionally created to hold old dirt)
- Large tracked/untracked content: data/ 1.0G, codebase.md 411M, .git 134M, .lh 5.1M
- Local-only files: credentials.json, Chinook.db, .envDemo, .env.example, ngrok.yml,
  mcp_config.json, local_cache/, many *.log files, stray dirs (`pygame.quit()`, `path`)
- Submodules: none

## What it is
DSPyGen: a Rails-inspired CLI for creating and deploying DSPy language-model pipelines.

## Classification
ACTIVE (census) — recent activity is dependabot only; WARM would also be defensible.

## Migration risk
- Unpushed preserve branch modep/preserve-20260926T1256Z-dspygen
- credentials.json (name only — likely an OAuth/service secret; never commit)
- data/ 1G and Chinook.db may be local-only datasets; codebase.md 411M is regenerable
Rating: MEDIUM

## Recommended action
COMMIT-PUSH
1. `cd /Users/sac/dev/dspygen && git push -u origin modep/preserve-20260926T1256Z-dspygen`
2. `git check-ignore -v credentials.json Chinook.db data codebase.md` — confirm ignored
3. DECISION: credentials.json — move to password manager; do not rsync in plain form
4. DECISION: data/ (1G) — rsync to archive volume if not re-downloadable
5. `rm -f codebase.md *.log file_2024-*.log` and `rm -rf .venv local_cache .lh` before copy
6. On new machine: `git clone https://github.com/seanchatmangpt/dspygen.git`

## First commands on the new machine
`poetry install && make test` (or `poetry run pytest`)

## See Also
- /Users/sac/docs/jira/v26.11.16/README.md
