from dspygen.meta import (
    MetaObservation,
    MetaProgram,
    MetaRefusal,
    ProcessSpec,
    StageSpec,
    greedy_cover,
    infer_process,
    second_order_candidates,
)


def test_process_inference_preserves_concurrency_and_reduces_transitivity():
    process = infer_process([
        ("observe", "admit", "plan", "verify"),
        ("observe", "plan", "admit", "verify"),
    ])
    stages = {stage.stage_id: stage for stage in process.stages}
    assert stages["admit"].requires == ("observe",)
    assert stages["plan"].requires == ("observe",)
    assert set(stages["verify"].requires) == {"admit", "plan"}


def test_cycle_is_refused_at_process_admission():
    try:
        ProcessSpec(
            "bad",
            (
                StageSpec("a", requires=("b",)),
                StageSpec("b", requires=("a",)),
            ),
        )
    except MetaRefusal as exc:
        assert exc.code == "META-CYCLIC-PROCESS"
    else:
        raise AssertionError("cyclic process was admitted")


def test_second_order_search_is_bounded_below_cartesian_space():
    dimensions = {
        "optimizer": ("identity", "mipro", "bootstrap"),
        "reasoning": ("predict", "cot", "react"),
        "temperature": ("low", "medium", "high"),
        "retrieval": ("off", "local", "hybrid"),
    }
    baseline = {name: values[0] for name, values in dimensions.items()}
    candidates = second_order_candidates(dimensions, baseline, "obs:1")
    assert len(candidates) == 33
    assert len(candidates) < 3**4
    portfolio = greedy_cover(candidates, max_candidates=7)
    assert 1 <= len(portfolio) <= 7


def test_runtime_executes_exact_admitted_dag_and_receipts_outputs():
    process = ProcessSpec(
        "demo",
        (
            StageSpec("observe", output_keys=("x",)),
            StageSpec("double", requires=("observe",), input_keys=("x",)),
        ),
    )
    observation = MetaObservation(
        subject="demo",
        revision="r1",
        examples_digest="examples:1",
        process_digest=process.digest,
    )
    program = MetaProgram(
        process,
        {
            "observe": lambda **_: {"x": 3},
            "double": lambda x: {"y": x * 2},
        },
    )
    context, receipt = program(observation)
    assert context["y"] == 6
    assert receipt.calls_used == 2
    assert receipt.standing == "ALIVE"
    assert receipt.receipt_id.startswith("meta-receipt:")
