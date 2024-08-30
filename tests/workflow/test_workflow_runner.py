import pytest
from dspygen.subcommands.wkf_cmd import run_workflows_in_directory
import os
from apscheduler.schedulers.background import BackgroundScheduler
import time

def test_run_workflows_in_directory(tmp_path):
    workflows_dir = tmp_path / "workflows"
    workflows_dir.mkdir()
    
    # Create a temporary directory structure with some YAML files
    (workflows_dir / "workflow1.yaml").write_text(f"""
name: TestWorkflow
triggers:
  - type: date
    run_date: now
jobs:
  - name: TestJob
    runner: python
    steps:
      - name: TestAction
        code: |
          print("hello world")
          import os
          output_dir = os.path.join('{tmp_path}', 'output')
          os.makedirs(output_dir, exist_ok=True)
          with open(os.path.join(output_dir, 'workflow1_output.txt'), 'w') as f:
            f.write('Integration test successful')
    """)
    (workflows_dir / "subdir").mkdir()
    (workflows_dir / "subdir" / "workflow2.yaml").write_text(f"""
name: TestWorkflow2
triggers:
  - type: date
    run_date: now
jobs:
  - name: TestJob2
    runner: python
    steps:
      - name: TestAction2
        code: |
          print("hello world 2")
          import os
          output_dir = os.path.join('{workflows_dir}/subdir', 'output')
          os.makedirs(output_dir, exist_ok=True)
          with open(os.path.join(output_dir, 'workflow2_output.txt'), 'w') as f:
            f.write('Integration 2 test successful')
    """)
    # Test with recursion
    scheduler = run_workflows_in_directory(str(workflows_dir), recursive=True)
    assert scheduler is not None
    jobs = scheduler.get_jobs()
    print(f"Number of jobs: {len(jobs)}")
    print(f"Jobs: {jobs}")
    assert len(jobs) == 2

    # Start the scheduler and wait for jobs to execute
    scheduler.start()
    time.sleep(2)  # Wait for 2 seconds to allow jobs to execute
    scheduler.shutdown()

    # Check if the output files were created
    output_file1 = tmp_path / "output" / "workflow1_output.txt"
    assert output_file1.exists()
    assert output_file1.read_text() == "Integration test successful"

    output_file2 = workflows_dir / "subdir" / "output" / "workflow2_output.txt"
    assert output_file2.exists()
    assert output_file2.read_text() == "Integration 2 test successful"

    # Test without recursion
    scheduler = run_workflows_in_directory(str(workflows_dir), recursive=False)
    assert scheduler is not None
    assert len(scheduler.get_jobs()) == 1

    # Test with empty directory
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    scheduler = run_workflows_in_directory(str(empty_dir))
    assert scheduler is None

    # Check if the output file was created
    output_file = tmp_path / "output" / "workflow1_output.txt"
    assert output_file.exists()
    assert output_file.read_text() == "Integration test successful"

    output_file = workflows_dir / "subdir" / "output" / "workflow2_output.txt"
    assert output_file.exists()
    assert output_file.read_text() == "Integration 2 test successful"
