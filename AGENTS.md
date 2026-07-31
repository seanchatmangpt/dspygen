# DSPyGen Agent Contract

This file is the sole normative agent contract for this repository.

## Law

DSPyGen changes follow `O → O* → A → R`.

- `O` is partial or stale observation.
- `O*` is admitted, aligned, complete, grounded, and bounded state.
- `A = μ(O*)` is a lawful manufactured artifact.
- `R` is the deterministic receipt that proves consequence and supports replay.

Admission and evidentiary standing are orthogonal. `RETIRED` is lifecycle only. It is never a standing.

## Canonical source and projections

The admitted architecture source is `.specify/dspygen-architecture.ttl`.
The manufacturing manifest is `ggen.toml`.
The ordered projection queries and Tera templates live under `.specify/queries/` and `.specify/templates/`.

The following are ggen-managed projection surfaces and must never be hand-edited:

- `src/dspygen/architecture/catalog.py`
- `docs/architecture/CATALOG.md`

There is no `generated/` tree. Projections land directly in canonical runtime and documentation paths.

To change a generated surface, edit the ontology, query, or template, then run:

```bash
ggen sync run --dry-run
ggen sync run
```

## Runtime boundary

`src/dspygen/architecture/model.py` is a pure deterministic kernel. It performs no filesystem, process, network, cloud, deployment, or package-install actuation.

All effectful execution intents are addressed to `BRCE`. DSPyGen may construct and validate intents. It does not execute them and does not define an alternate broker or recovery rail.

## Standing

Permitted repository judgments are:

- `PARTIAL_ALIVE`
- `ALIVE`
- `BLOCKED`
- `BUILD_BROKEN`
- `UNKNOWN`
- `UNSUPPORTED`

`ALIVE` requires all five evidence surfaces:

1. positive witness
2. negative falsifier
3. independent verifier
4. receipt verifier
5. replay

A green build alone cannot establish semantic correctness. A generated artifact cannot prove its own generator.

## Verification ladder

Run the narrow verifier first, then expand:

```bash
PYTHONPATH=src python -m unittest discover -s tests/architecture -v
PYTHONPATH=src python scripts/verify_architecture.py
```

Then run repository-wide unit, integration, end-to-end, chaos, stress, benchmark, and verifier-report rails when the change touches those surfaces.

## Git and evidence safety

- Resolve and record the exact base SHA before editing.
- Keep diffs bounded to the admitted task.
- Do not hand-edit generated outputs.
- Do not weaken tests, coverage, or refusal gates to obtain green status.
- No status claim without observed execution evidence.
- Publish changes as a draft PR until the exact-head verifier is green.
