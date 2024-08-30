import pytest
from dspygen.subcommands.wkf_cmd import run_workflows_in_directory

def test_run_workflows_in_directory(tmp_path):
    # Create a temporary directory structure with some YAML files
    (tmp_path / "workflow1.yaml").write_text("# Test workflow 1")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "workflow2.yaml").write_text("# Test workflow 2")

    # Test with recursion
    scheduler = run_workflows_in_directory(str(tmp_path), recursive=True)
    assert scheduler is not None
    assert len(scheduler.get_jobs()) == 2

    # Test without recursion
    scheduler = run_workflows_in_directory(str(tmp_path), recursive=False)
    assert scheduler is not None
    assert len(scheduler.get_jobs()) == 1

    # Test with empty directory
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    scheduler = run_workflows_in_directory(str(empty_dir))
    assert scheduler is None