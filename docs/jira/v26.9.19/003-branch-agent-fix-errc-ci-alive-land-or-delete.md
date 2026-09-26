# dspygen: land or delete remote branch `agent/fix-errc-ci-alive`

- Standing: OPEN
- Created: 2026-09-19 (v26.9.19 gh survey wave)
- Source: remote branch `agent/fix-errc-ci-alive` — not merged into `main`, no open PR
- Evidence: `git branch -r --no-merged origin/main` lists it; absent from `gh pr list` heads

## Work to complete
- Decide: open a PR (`gh pr create -R seanchatmangpt/dspygen --head agent/fix-errc-ci-alive`) or delete (`git push origin --delete agent/fix-errc-ci-alive`).
- If superseded, delete; otherwise land through review.

## Acceptance
- After `git fetch --prune`, `git branch -r --no-merged origin/main` no longer lists `agent/fix-errc-ci-alive`.

## History
- 2026-09-19 | OPEN | survey found PR-less unmerged branch | agent/fix-errc-ci-alive | decision pending
