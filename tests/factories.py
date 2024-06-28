import factory
from factory import Faker, SubFactory
from datetime import datetime, timedelta
from pydantic import HttpUrl, Field
from typing import Optional, List, Dict, Any

from dspygen.models.jira_models import (
    JiraUser, JiraPriority, JiraStatusCategory, JiraStatus, JiraIssueType,
    JiraProject, JiraComponent, JiraVersion, JiraComment, JiraAttachment,
    JiraResolution, JiraWorklog, JiraTimetracking, JiraIssueFields, JiraIssue
)


class JiraUserFactory(factory.Factory):
    class Meta:
        model = JiraUser

    self = Faker('url')
    accountId = Faker('uuid4')
    accountType = Faker('random_element', elements=['atlassian', 'app'])
    emailAddress = Faker('email')
    displayName = Faker('name')
    active = Faker('boolean')
    timeZone = Faker('timezone')
    avatarUrls = factory.Dict({
        '48x48': Faker('url'),
        '24x24': Faker('url'),
        '16x16': Faker('url'),
        '32x32': Faker('url')
    })


class JiraPriorityFactory(factory.Factory):
    class Meta:
        model = JiraPriority

    self = Faker('url')
    iconUrl = Faker('url')
    name = Faker('word')
    id = Faker('uuid4')


class JiraStatusCategoryFactory(factory.Factory):
    class Meta:
        model = JiraStatusCategory

    self = Faker('url')
    id = Faker('random_int')
    key = Faker('word')
    colorName = Faker('color_name')
    name = Faker('word')


class JiraStatusFactory(factory.Factory):
    class Meta:
        model = JiraStatus

    self = Faker('url')
    description = Faker('sentence')
    iconUrl = Faker('url')
    name = Faker('word')
    id = Faker('uuid4')
    statusCategory = SubFactory(JiraStatusCategoryFactory)


class JiraIssueTypeFactory(factory.Factory):
    class Meta:
        model = JiraIssueType

    self = Faker('url')
    id = Faker('uuid4')
    description = Faker('sentence')
    iconUrl = Faker('url')
    name = Faker('word')
    subtask = Faker('boolean')
    avatarId = factory.Maybe('subtask', yes_declaration=Faker('random_int'), no_declaration=None)


class JiraProjectFactory(factory.Factory):
    class Meta:
        model = JiraProject

    self = Faker('url')
    id = Faker('uuid4')
    key = Faker('word')
    name = Faker('word')
    projectTypeKey = Faker('word')


class JiraComponentFactory(factory.Factory):
    class Meta:
        model = JiraComponent

    self = Faker('url')
    id = Faker('uuid4')
    name = Faker('word')


class JiraVersionFactory(factory.Factory):
    class Meta:
        model = JiraVersion

    self = Faker('url')
    id = Faker('uuid4')
    name = Faker('word')


class JiraCommentFactory(factory.Factory):
    class Meta:
        model = JiraComment

    self = Faker('url')
    id = Faker('uuid4')
    author = SubFactory(JiraUserFactory)
    body = Faker('paragraph')
    updateAuthor = SubFactory(JiraUserFactory)
    created = Faker('date_time_this_decade')
    updated = Faker('date_time_this_decade')


class JiraAttachmentFactory(factory.Factory):
    class Meta:
        model = JiraAttachment

    self = Faker('url')
    id = Faker('uuid4')
    filename = Faker('file_name')
    author = SubFactory(JiraUserFactory)
    created = Faker('date_time_this_decade')
    size = Faker('random_int')
    mimeType = Faker('mime_type')
    content = Faker('url')
    thumbnail = factory.Maybe('mimeType', yes_declaration=Faker('url'), no_declaration=None)


class JiraResolutionFactory(factory.Factory):
    class Meta:
        model = JiraResolution

    self = Faker('url')
    id = Faker('uuid4')
    description = Faker('sentence')
    name = Faker('word')


class JiraWorklogFactory(factory.Factory):
    class Meta:
        model = JiraWorklog

    self = Faker('url')
    author = SubFactory(JiraUserFactory)
    updateAuthor = SubFactory(JiraUserFactory)
    comment = factory.Maybe('author', yes_declaration=Faker('paragraph'), no_declaration=None)
    created = Faker('date_time_this_decade')
    updated = Faker('date_time_this_decade')
    started = Faker('date_time_this_decade')
    timeSpent = factory.LazyFunction(lambda: format_timedelta(fake.time_delta(end_datetime='+30d')))
    timeSpentSeconds = Faker('random_int')
    id = Faker('uuid4')
    issueId = Faker('uuid4')


def format_timedelta(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

from faker import Faker as FakerGenerator

fake = FakerGenerator()

class JiraTimetrackingFactory(factory.Factory):
    class Meta:
        model = JiraTimetracking

    originalEstimate = factory.LazyFunction(lambda: format_timedelta(fake.time_delta(end_datetime='+30d')))
    remainingEstimate = factory.LazyFunction(lambda: format_timedelta(fake.time_delta(end_datetime='+30d')))
    timeSpent = factory.LazyFunction(lambda: format_timedelta(fake.time_delta(end_datetime='+30d')))
    originalEstimateSeconds = Faker('random_int')
    remainingEstimateSeconds = Faker('random_int')
    timeSpentSeconds = Faker('random_int')


class JiraIssueFieldsFactory(factory.Factory):
    class Meta:
        model = JiraIssueFields

    summary = Faker('sentence')
    description = factory.Maybe('summary', yes_declaration=Faker('paragraph'), no_declaration=None)
    created = Faker('date_time_this_decade')
    updated = Faker('date_time_this_decade')
    project = SubFactory(JiraProjectFactory)
    issuetype = SubFactory(JiraIssueTypeFactory)
    status = SubFactory(JiraStatusFactory)
    priority = factory.Maybe('status', yes_declaration=SubFactory(JiraPriorityFactory), no_declaration=None)
    assignee = factory.Maybe('status', yes_declaration=SubFactory(JiraUserFactory), no_declaration=None)
    reporter = SubFactory(JiraUserFactory)
    labels = factory.List([Faker('word') for _ in range(3)])
    comments = factory.List([SubFactory(JiraCommentFactory) for _ in range(3)])
    attachments = factory.List([SubFactory(JiraAttachmentFactory) for _ in range(2)])
    resolution = factory.Maybe('status', yes_declaration=SubFactory(JiraResolutionFactory), no_declaration=None)
    worklog = factory.List([SubFactory(JiraWorklogFactory) for _ in range(3)])
    timetracking = factory.Maybe('status', yes_declaration=SubFactory(JiraTimetrackingFactory), no_declaration=None)
    components = factory.List([SubFactory(JiraComponentFactory) for _ in range(2)])
    versions = factory.List([SubFactory(JiraVersionFactory) for _ in range(2)])
    fixVersions = factory.List([SubFactory(JiraVersionFactory) for _ in range(2)])
    duedate = factory.Maybe('status', yes_declaration=Faker('date'), no_declaration=None)
    # customfield_11440 = factory.List([Faker('pydict', nb_elements=2) for _ in range(2)])
    # customfield_11441 = factory.Maybe('status', yes_declaration=Faker('date'), no_declaration=None)
    # customfield_11442 = factory.Maybe('status', yes_declaration=Faker('date_time'), no_declaration=None)
    # customfield_11443 = factory.List([Faker('word') for _ in range(3)])
    # customfield_11444 = factory.Maybe('status', yes_declaration=Faker('random_int'), no_declaration=None)
    # customfield_11445 = factory.Maybe('status', yes_declaration=factory.Dict({str: Faker('word')}), no_declaration=None)
    # customfield_11447 = factory.Dict({str: Faker('word')})
    # customfield_11448 = factory.List([Faker('pydict', nb_elements=2) for _ in range(2)])
    # customfield_11449 = factory.Maybe('status', yes_declaration=factory.Dict({str: Faker('word')}), no_declaration=None)
    # customfield_11450 = factory.Maybe('status', yes_declaration=Faker('paragraph'), no_declaration=None)
    # customfield_11452 = factory.Maybe('status', yes_declaration=Faker('url'), no_declaration=None)
    # customfield_11453 = factory.Maybe('status', yes_declaration=factory.Dict({str: Faker('word')}), no_declaration=None)
    # customfield_11458 = factory.List([Faker('pydict', nb_elements=2) for _ in range(2)])
    # customfield_10700 = factory.List([Faker('word') for _ in range(3)])


class JiraIssueFactory(factory.Factory):
    class Meta:
        model = JiraIssue

    id = Faker('uuid4')
    self = Faker('url')
    key = Faker('word')
    fields = SubFactory(JiraIssueFieldsFactory)


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    # Create instances of each factory and print them for validation
    user_instance = JiraUserFactory()
    priority_instance = JiraPriorityFactory()
    status_category_instance = JiraStatusCategoryFactory()
    issue_instance = JiraIssueFactory()

    print("JiraUserFactory instance:", user_instance)
    print("JiraPriorityFactory instance:", priority_instance)
    print("JiraStatusCategoryFactory instance:", status_category_instance)
    print("JiraIssueFactory instance:", issue_instance)


if __name__ == '__main__':
    main()
