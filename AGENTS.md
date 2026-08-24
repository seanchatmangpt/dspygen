# DSPyGen Agent Contract

This file is the sole normative agent contract for this repository.

## Constitutional law

DSPyGen changes follow:

```text
O → O* → candidate lattice → verified candidate → authorized plan
→ intent → broker → observed consequence → causal receipt → replay → standing
```

```text
A = μ(O*)
R = receipt(A)
```

Preserve the live system before replacement. Unknown fences remain `UNKNOWN`; they are not permission to delete. Candidate, verified, authorized, planned, actuated, consequence-verified, receipted, and replayed are distinct states. No object implicitly acquires the authority of its successor.

## Canonical authority

The architecture authorities are:

- `.specify/dspygen-architecture.ttl` — ggen projection authority;
- `.specify/cmd/repository.ttl` — CMD semantic authority;
- `.specify/cmd/shapes/cmd-shapes.ttl` — structural admission boundary;
- `.specify/cmd/architecture.toml` — bounded internal/external dimensions, constraints, resources, passports, and broker controls;
- `.specify/cmd/authority.toml` — exact-tree ownership and Chesterton-fence policy;
- `packs/cmd-packs.json` — immutable atomic capability pack catalog;
- `bblocks/cmd-dspygen-complete.json` — receipted Building Block composition;
- `.ggen/packs.lock` — exact pack closure and digests.

The ggen-managed projections below must not be hand-edited:

- `src/dspygen/architecture/catalog.py`
- `docs/architecture/CATALOG.md`

There is no root `generated/` authority tree. Projections land in canonical paths.

## Pure kernel and adapters

`src/dspygen/architecture/model.py` and `src/dspygen/architecture/cmd_kernel.py` are deterministic kernels. They import no filesystem actuator, process runner, network client, provider SDK, credential source, or deployment adapter.

Adapters may represent lawful objects. Adapters must not silently become actuators.

## Internal actuation

Local mutation is confined to `cmd_materializer.py` and follows:

```text
verified candidate → exact local grant → plan → intent receipt
→ bounded immutable staging → validation → result receipt
→ atomic manifest-pointer publication → re-observation → replay
```

Path and ownership admission precede writes. No visible managed payload may survive without its durable result receipt. Every injected interruption must leave the publication pointer unchanged.

## External actuation

All external effects cross `BRCE`. The external rail requires:

- typed inert intent;
- exact grant and current-state precondition;
- action/resource-scoped consent;
- identity, trust, data-class, and jurisdiction closure;
- resource, retry, circuit, and error budgets;
- idempotency;
- independent postcondition observation;
- predecessor-linked causal receipt.

Hooks manufacture intents only. They cannot deploy, publish, mutate databases, authorize, or assign standing. Automatic and autonomic operation use this same rail; there is no emergency bypass.

## Gall standing

Permitted standing values are:

- `PARTIAL_ALIVE`
- `ALIVE`
- `BLOCKED`
- `BUILD_BROKEN`
- `UNKNOWN`
- `UNSUPPORTED`

Lifecycle is orthogonal. `ALIVE` requires all five evidence surfaces:

1. positive witness;
2. negative falsifier;
3. independent verifier;
4. receipt verifier;
5. deterministic replay.

The executor may publish evidence. Only the independent verifier publishes aggregate local standing. External standing remains `UNKNOWN` until external evidence is independently admitted.

## G0–G9 checkpoints

- G0: exact Git-object census;
- G1: total authority and Chesterton-fence map;
- G2: ontology, SHACL, standing vocabulary, and typed refusals;
- G3: bounded internal candidate lattice and coverage;
- G4: external identity/consent/trust/jurisdiction/consequence lattice;
- G5: immutable packs, Building Blocks, deterministic closure, and lockfile;
- G6: pure shared kernel and non-mutating planning;
- G7: transactional local materialization, rollback classification, chaos proof;
- G8: BRCE grants, consent, budgets, postconditions, external receipts;
- G9: self-observation, byte identity, clean exact-head detached replay, crown report.

No checkpoint may inflate a later checkpoint. Pending work remains visible as `PARTIAL_ALIVE` or `UNKNOWN`.

## Stable operational routes

```bash
python -m dspygen.architecture.cmd_entry observe
python -m dspygen.architecture.cmd_entry fence-verify
python -m dspygen.architecture.cmd_entry ontology-validate
python -m dspygen.architecture.cmd_entry candidates-enumerate --domain internal
python -m dspygen.architecture.cmd_entry candidates-coverage --domain external
python -m dspygen.architecture.cmd_entry plan --domain internal
python -m dspygen.architecture.cmd_entry materialize --domain internal --grant local-filesystem-broker --output-root <directory>
python -m dspygen.architecture.cmd_entry receipt-verify --receipt <receipt.json>
python -m dspygen.architecture.cmd_entry replay --receipt <receipt.json>
python -m dspygen.architecture.cmd_entry verifier-report
python -m dspygen.architecture.cmd_entry crown
```

Every route emits machine-readable JSON. The preserved `dspygen architecture verify` and `dspygen architecture intent` routes retain their prior contracts.

## Verification ladder

Run narrow to broad:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/architecture -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/cmd -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/verify_architecture.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/run_cmd_verifier.py --exact-head-sha "$(git rev-parse HEAD)"
```

The exact-head CI crown must additionally execute a detached clean-tree replay. Protocol/unit, property, integration, black-box E2E, security, chaos, stress, benchmark, replay, and verifier-report evidence remain distinct suites.

## Git and evidence safety

- Resolve and record the exact base SHA before editing.
- Observe Git modes and object types; do not infer authority from directory names.
- Keep diffs bounded to the admitted task.
- Do not hand-edit generated projections.
- Do not weaken tests, budgets, ownership, consent, or refusal gates to obtain green status.
- Do not delete or consolidate workflows before G0/G1 ownership and retirement fences exist.
- No status claim without observed execution evidence.
- Keep pull requests draft until exact-head detached replay succeeds.
