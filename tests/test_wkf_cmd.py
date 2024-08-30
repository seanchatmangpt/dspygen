import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from dspygen.subcommands.wkf_cmd import app, run_workflows_in_directory
from dspygen.workflow.workflow_models import Workflow
from apscheduler.schedulers.background import BackgroundScheduler

runner = CliRunner()

@pytest.fixture
def mock_workflow():
    return MagicMock(spec=Workflow)

@pytest.fixture
def mock_scheduler():
    return MagicMock(spec=BackgroundScheduler)

def test_run_workflow(mock_workflow):
    with patch('dspygen.subcommands.wkf_cmd.Workflow.from_yaml', return_value=mock_workflow) as mock_from_yaml, \
         patch('dspygen.subcommands.wkf_cmd.execute_workflow') as mock_execute:
        
        result = runner.invoke(app, ["run", "test_workflow.yaml"])
        
        assert result.exit_code == 0
        mock_from_yaml.assert_called_once_with("test_workflow.yaml")
        mock_execute.assert_called_once_with(mock_workflow)

def test_run_workflows_in_directory(tmp_path, mock_workflow, mock_scheduler):
    # Create test YAML files
    (tmp_path / "workflow1.yaml").write_text("# Test workflow 1")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "workflow2.yaml").write_text("# Test workflow 2")

    with patch('dspygen.subcommands.wkf_cmd.Workflow.from_yaml', return_value=mock_workflow), \
         patch('dspygen.subcommands.wkf_cmd.BackgroundScheduler', return_value=mock_scheduler), \
         patch('dspygen.subcommands.wkf_cmd.schedule_workflow') as mock_schedule:
        
        # Test with recursion
        scheduler = run_workflows_in_directory(str(tmp_path), recursive=True)
        assert scheduler == mock_scheduler
        assert mock_schedule.call_count == 2
        
        # Reset mocks
        mock_schedule.reset_mock()
        mock_scheduler.reset_mock()
        
        # Test without recursion
        scheduler = run_workflows_in_directory(str(tmp_path), recursive=False)
        assert scheduler == mock_scheduler
        assert mock_schedule.call_count == 1

        # Test with empty directory
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        with patch('dspygen.subcommands.wkf_cmd.BackgroundScheduler', return_value=mock_scheduler):
            scheduler = run_workflows_in_directory(str(empty_dir))
            assert scheduler is None
            mock_scheduler.shutdown.assert_called_once()

@pytest.mark.parametrize("recursive", [True, False])
def test_run_all_command(recursive, mock_scheduler):
    with patch('dspygen.subcommands.wkf_cmd.run_workflows_in_directory', return_value=mock_scheduler) as mock_run:
        result = runner.invoke(app, ["run-all", ".", f"--{'no-' if not recursive else ''}recursive"])
        
        assert result.exit_code == 0
        mock_run.assert_called_once_with(".", recursive=recursive)
        mock_scheduler.start.assert_called_once()
        mock_scheduler.print_jobs.assert_called_once()

def test_run_all_command_no_workflows():
    with patch('dspygen.subcommands.wkf_cmd.run_workflows_in_directory', return_value=None) as mock_run:
        result = runner.invoke(app, ["run-all", "."])
        
        assert result.exit_code == 0

def test_trigger_workflow(mock_workflow):
    with patch('dspygen.subcommands.wkf_cmd.Workflow.from_yaml', return_value=mock_workflow) as mock_from_yaml, \
         patch('dspygen.subcommands.wkf_cmd.execute_workflow') as mock_execute, \
         patch('dspygen.subcommands.wkf_cmd.os.path.exists', return_value=True):
        
        result = runner.invoke(app, ["trigger", "test_workflow"])
        
        assert result.exit_code == 0
        mock_from_yaml.assert_called_once()
        mock_execute.assert_called_once_with(mock_workflow)
        assert "Workflow test_workflow triggered" in result.output
