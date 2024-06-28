import pytest
from pathlib import Path

from dspygen.models.jira_models import JiraIssueRepository
from factories import (
    JiraIssueFactory, JiraUserFactory, JiraPriorityFactory, JiraStatusCategoryFactory,
    JiraStatusFactory, JiraIssueTypeFactory, JiraProjectFactory, JiraComponentFactory,
    JiraVersionFactory, JiraCommentFactory, JiraAttachmentFactory, JiraResolutionFactory,
    JiraWorklogFactory, JiraTimetrackingFactory, JiraIssueFieldsFactory
)


@pytest.fixture
def storage_file(tmp_path) -> Path:
    return tmp_path / "issues.json"


@pytest.fixture
def repository(storage_file: Path) -> JiraIssueRepository:
    return JiraIssueRepository(storage_file)


@pytest.fixture
def issue() -> JiraIssueFactory:
    return JiraIssueFactory()


def test_create(repository: JiraIssueRepository, issue: JiraIssueFactory):
    repository.create(issue)
    assert repository.read(id=issue.id) == issue


def test_read(repository: JiraIssueRepository, issue: JiraIssueFactory):
    repository.create(issue)
    retrieved_issue = repository.read(id=issue.id)
    assert retrieved_issue == issue
    assert repository.read(id="nonexistent") is None


def test_delete(repository: JiraIssueRepository, issue: JiraIssueFactory):
    repository.create(issue)
    assert repository.delete(id=issue.id) is True
    assert repository.read(id=issue.id) is None
    assert repository.delete(id="nonexistent") is False


def test_update(repository: JiraIssueRepository, issue: JiraIssueFactory):
    repository.create(issue)
    updated_issue = issue.copy(update={"key": "UPDATED-1"})
    repository.update(updated_issue)
    assert repository.read(id=issue.id).key == "UPDATED-1"


def test_upsert_create(repository: JiraIssueRepository, issue: JiraIssueFactory):
    repository.upsert(issue)
    assert repository.read(id=issue.id) == issue


def test_upsert_update(repository: JiraIssueRepository, issue: JiraIssueFactory):
    repository.create(issue)
    updated_issue = issue.copy(update={"key": "UPDATED-1"})
    repository.upsert(updated_issue)
    assert repository.read(id=issue.id).key == "UPDATED-1"


def test_read_all(repository: JiraIssueRepository, issue: JiraIssueFactory):
    repository.create(issue)
    all_issues = repository.read_all()
    assert len(all_issues) == 1
    assert all_issues[0] == issue
