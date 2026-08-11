# DSPyGen Meta-Framework

`dspygen.meta` turns the reusable control-plane ideas from AutoFDE-Lab into a DSPy-native meta-programming layer. It is intentionally **not** another agent loop.

## Process science over prompt plumbing

The framework separates four concerns:

1. **Infer / declare a process** as a partial order of stages.
2. **Admit a design space** of DSPy choices without materializing the full Cartesian product.
3. **Execute selectively** under explicit experiment and runtime bounds.
4. **Receipt the consequence** with identities for the process, observation, candidate and stage outputs.

The core correspondence is:

```text
AutoFDE-Lab                         DSPyGen meta
-------------------------------     -----------------------------------
PhaseGraph / work partial order  -> ProcessSpec / StageSpec
admission-time graph validation  -> typed MetaRefusal
C2 DecisionBasis compiler        -> second_order_candidates()
bounded covering design          -> greedy_cover()
work-execution scheduler         -> MetaProgram
observable traces                -> infer_process()
Definition-of-Done evidence      -> ExperimentResult + MetaReceipt
```

## Process inference

Successful traces can be lifted into a partial order rather than copied into a false total order. If `A` precedes `B` in the evidence and no trace demonstrates `B` before `A`, the edge is admitted. If both directions are observed, the framework preserves the pair as potentially concurrent. Transitive edges are reduced.

## Combinatorial DSPy search

For dimensions `D1..Dn`, the framework represents the baseline plus one- and two-factor substitutions:

```text
C2(d0) = {d0} U {one-factor changes} U {two-factor changes}
```

This preserves pairwise interactions at polynomial construction cost instead of materializing `D1 x ... x Dn`. A deterministic greedy cover then selects a bounded experiment portfolio.

Typical DSPy dimensions include optimizer, module topology, reasoning mode, retrieval policy, LM family, temperature policy, demonstration policy and metric policy. Constraints are predicates applied before a candidate can enter the experiment portfolio.

## DSPy adapter

`configure_dspy_candidate()` maps a candidate onto a caller-supplied optimizer registry. DSPy remains responsible for compiling and predicting; the meta-framework owns process identity, search topology, bounds and evidence. No candidate has ambient execution authority.

## Packaging and replay

The repository uses `uv` as its dependency authority. `pyproject.toml` declares compatibility; `uv.lock` declares the exact resolved environment. CI manufactures and validates the lock as a dependency receipt, allowing a later frozen replay with `uv sync --frozen`.
