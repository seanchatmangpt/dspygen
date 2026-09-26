# dspygen: commit or clean uncommitted changes

- Standing: OPEN
- Created: 2026-09-19 (v26.9.19 gh survey wave)
- Source: working tree dirty at survey time
- Evidence: `git status --porcelain` → 35 path(s) (tracked-modified: 33, untracked: 2); sample: A Example_meeting_ABC_Corporation_John_Doe_XYZ_Inc_Jane_Smith_DEF_Agency_Bob_Johnson.toml; M pyproject.toml; D src/dspygen/agents/__init__.py;?? src/dspygen/lm/groq_lm_v3.py;?? tests/test_groq_lm_v3.p

## Work to complete
- Review the 33 tracked-modified path(s); commit them as atomic pieces on a purpose branch, or revert what is transient.
- For the 2 untracked path(s): add intentional files to git and commit; gitignore or delete build artifacts/temp files.
- Note: this survey's ticket files under docs/jira/v26.9.19/ are intentionally uncommitted; include or exclude them deliberately in the commit plan.

## Acceptance
- `git status --porcelain` is clean (except items deliberately deferred and recorded here).

## History
- 2026-09-19 | OPEN | survey found dirty tree | 35 paths (T33/U2) | commit/clean pending
