# dspygen: land or delete remote branch `agent/scratch-ci-closeout`

- Standing: OPEN
- Created: 2026-09-19 (v26.9.19 gh survey wave)
- Source: remote branch `agent/scratch-ci-closeout` — not merged into `main`, no open PR
- Evidence: `git branch -r --no-merged origin/main` lists it; absent from `gh pr list` heads

## Work to complete
- Decide: open a PR (`gh pr create -R seanchatmangpt/dspygen --head agent/scratch-ci-closeout`) or delete (`git push origin --delete agent/scratch-ci-closeout`).
- If superseded, delete; otherwise land through review.

## Acceptance
- After `git fetch --prune`, `git branch -r --no-merged origin/main` no longer lists `agent/scratch-ci-closeout`.

## History
- 2026-09-19 | OPEN | survey found PR-less unmerged branch | agent/scratch-ci-closeout | decision pending
