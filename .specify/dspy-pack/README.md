# DSPy ggen pack connection

This directory is an isolated ggen consumer project for DSPyGen's DSPy program-manufacturing surface.

The pack dependency is pinned to:

- repository: `seanchatmangpt/ggen-marketplace`
- commit: `465e9462747e489be842c7107fdf537735de5d65`
- subdirectory: `packs/dspy-pack`
- pack version: `0.2.0`
- qualifying ggen runtime: `v26.8.8`

`ontology.ttl` is the authored consumer graph. `ggen sync run` projects that graph through `dspy-pack`; generated Python is a consequence and is not checked in as a second source of truth.

## Authority boundary

The admitted DSPyGen consumer currently declares only `ChainOfThought`. It manufactures a candidate POWL description. It does not admit or execute that candidate.

`ReAct` is intentionally absent here even though dspy-pack 0.2.0 supports it. MCP-backed tool calls remain fenced until they are converted into inert intents and routed through DSPyGen's BRCE rail. The pack therefore cannot create a second DO path.

## Replay

From this directory, with `ggen v26.8.8` available:

```bash
ggen sync run
python ../../../scripts/verify_dspy_ggen_pack.py --project . --rendered src/dspy_program.py
```

For repository verification, CI copies this project to a temporary directory before rendering so no generated output is added to the source tree.
