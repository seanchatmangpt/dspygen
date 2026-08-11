# DSPy 80/20 ERRC Max — built with ggen dspy-pack

This is a consumer of the existing `ggen` DSPy pack. It does not modify or fork the pack.

The consumer ontology preserves reversible DSPy alternatives before selection:

- reasoning: Predict, ChainOfThought, ProgramOfThought, RLM;
- composition/retrieval: Pipeline with Retrieve -> ChainOfThought;
- optimizer families: COPRO, MIPROv2, SIMBA, InferRules, LabeledFewShot;
- optimizer discrimination: the five optimizer families are instantiated independently over both Predict and ChainOfThought, yielding ten explicit optimizer experiments;
- LM configuration is explicit in RDF rather than hidden in imperative Python.

The construction path is:

`ontology.ttl -> pinned dspy-pack -> ggen sync run -> src/dspy_program.py + src/dspy_optimize.py -> verify.py`

`src/dspy_program.py` and `src/dspy_optimize.py` are projections manufactured by the pack during validation. The canonical source is `ontology.ttl`; no `generated/` directory or `generated.py` surface is admitted.

Authority boundary: this experiment is `CONSTRUCT_ONLY`; model/provider actuation is not required for the construction proof and is refused by the validation court.
