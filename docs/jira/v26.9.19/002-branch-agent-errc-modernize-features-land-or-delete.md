# dspygen: land or delete remote branch `agent/errc-modernize-features`

- Standing: OPEN
- Created: 2026-09-19 (v26.9.19 gh survey wave)
- Source: remote branch `agent/errc-modernize-features` — not merged into `main`, no open PR
- Evidence: `git branch -r --no-merged origin/main` lists it; absent from `gh pr list` heads

## Work to complete
- Decide: open a PR (`gh pr create -R seanchatmangpt/dspygen --head agent/errc-modernize-features`) or delete (`git push origin --delete agent/errc-modernize-features`).
- If superseded, delete; otherwise land through review.

## Acceptance
- After `git fetch --prune`, `git branch -r --no-merged origin/main` no longer lists `agent/errc-modernize-features`.

## History
- 2026-09-19 | OPEN | survey found PR-less unmerged branch | agent/errc-modernize-features | decision pending
