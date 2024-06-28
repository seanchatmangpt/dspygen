from pathlib import Path

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

from dspygen.rdddy.base_repository import BaseRepository


class JiraUser(BaseModel):
    self: HttpUrl
    accountId: str
    accountType: str
    emailAddress: Optional[EmailStr]
    displayName: str
    active: bool
    timeZone: str
    avatarUrls: Dict[str, HttpUrl]


class JiraPriority(BaseModel):
    self: HttpUrl
    iconUrl: HttpUrl
    name: str
    id: str


class JiraStatusCategory(BaseModel):
    self: HttpUrl
    id: int
    key: str
    colorName: str
    name: str


class JiraStatus(BaseModel):
    self: HttpUrl
    description: str
    iconUrl: HttpUrl
    name: str
    id: str
    statusCategory: JiraStatusCategory


class JiraIssueType(BaseModel):
    self: HttpUrl
    id: str
    description: str
    iconUrl: HttpUrl
    name: str
    subtask: bool
    avatarId: Optional[int]


class JiraProject(BaseModel):
    self: HttpUrl
    id: str
    key: str
    name: str
    projectTypeKey: str


class JiraComponent(BaseModel):
    self: HttpUrl
    id: str
    name: str


class JiraVersion(BaseModel):
    self: HttpUrl
    id: str
    name: str


class JiraComment(BaseModel):
    self: HttpUrl
    id: str
    author: JiraUser
    body: str
    updateAuthor: JiraUser
    created: datetime
    updated: datetime


class JiraAttachment(BaseModel):
    self: HttpUrl
    id: str
    filename: str
    author: JiraUser
    created: datetime
    size: int
    mimeType: str
    content: HttpUrl
    thumbnail: Optional[HttpUrl]


class JiraResolution(BaseModel):
    self: HttpUrl
    id: str
    description: str
    name: str


class JiraWorklog(BaseModel):
    self: HttpUrl
    author: JiraUser
    updateAuthor: JiraUser
    comment: Optional[str]
    created: datetime
    updated: datetime
    started: datetime
    timeSpent: str
    timeSpentSeconds: int
    id: str
    issueId: str


class JiraTimetracking(BaseModel):
    originalEstimate: Optional[str]
    remainingEstimate: Optional[str]
    timeSpent: Optional[str]
    originalEstimateSeconds: Optional[int]
    remainingEstimateSeconds: Optional[int]
    timeSpentSeconds: Optional[int]


class JiraIssueFields(BaseModel):
    summary: str
    description: Optional[str]
    created: datetime
    updated: datetime
    project: JiraProject
    issuetype: JiraIssueType
    status: JiraStatus
    priority: Optional[JiraPriority]
    assignee: Optional[JiraUser]
    reporter: JiraUser
    labels: List[str] = Field(default_factory=list)
    comments: Optional[List[JiraComment]] = Field(default_factory=list)
    attachments: Optional[List[JiraAttachment]] = Field(default_factory=list)
    resolution: Optional[JiraResolution] = None
    worklog: Optional[List[JiraWorklog]] = Field(default_factory=list)
    timetracking: Optional[JiraTimetracking] = None
    components: Optional[List[JiraComponent]] = None
    versions: Optional[List[JiraVersion]] = None
    fixVersions: Optional[List[JiraVersion]] = None
    duedate: Optional[str] = None  # Format: 'YYYY-MM-DD'
    customfield_11440: Optional[List[Dict[str, str]]] = None  # Checkbox custom field
    customfield_11441: Optional[str] = None  # Date picker custom field
    customfield_11442: Optional[str] = None  # Date time picker custom field
    customfield_11443: Optional[List[str]] = None  # Labels custom field
    customfield_11444: Optional[int] = None  # Number custom field
    customfield_11445: Optional[Dict[str, str]] = None  # Radio button custom field
    customfield_11447: Optional[Dict[str, Any]] = None  # Cascading select custom field
    customfield_11448: Optional[List[Dict[str, str]]] = None  # Multi-select custom field
    customfield_11449: Optional[Dict[str, str]] = None  # Single-select custom field
    customfield_11450: Optional[str] = None  # Multi-line text custom field
    customfield_11452: Optional[str] = None  # URL custom field
    customfield_11453: Optional[Dict[str, str]] = None  # Single-user picker custom field
    customfield_11458: Optional[List[Dict[str, str]]] = None  # Multi-user picker custom field
    customfield_10700: Optional[List[str]] = None  # Elements Connect (formerly nFeed) custom field


class JiraIssue(BaseModel):
    id: str
    self: HttpUrl
    key: str
    fields: JiraIssueFields


class JiraIssueRepository(BaseRepository[JiraIssue]):
    def __init__(self, storage_file: Path):
        super().__init__(JiraIssue, storage_file)


def main():
    """Main function"""


if __name__ == '__main__':
    main()
