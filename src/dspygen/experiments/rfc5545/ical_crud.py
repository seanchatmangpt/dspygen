from datetime import datetime
from typing import List

from icontract import require, ensure

import uuid

from sqlmodel import Session

from dspygen.utils.crud_tools import *

from dspygen.experiments.rfc5545.ical_models import *

delete = True


# Create a new journal entry
@require(lambda dtstamp: isinstance(dtstamp, datetime))
@require(lambda dtstart: dtstart is None or isinstance(dtstart, datetime))
@require(lambda summary: summary is None or isinstance(summary, str))
@require(lambda description: description is None or isinstance(description, str))
@require(lambda calendar_id: calendar_id is None or isinstance(calendar_id, int))
@ensure(lambda result: result.id is not None)
def create_journal(
    dtstart: datetime = None,
    summary: str = None,
    description: str = None,
    calendar_id: int = None,
) -> Journal:
    journal = Journal(
        uid=str(uuid.uuid4()),
        dtstamp=datetime.utcnow(),
        dtstart=dtstart,
        summary=summary,
        description=description,
        calendar_id=calendar_id,
    )
    add_model(journal)
    return journal


# Read a journal entry by its ID
@require(lambda journal_id: isinstance(journal_id, int))
@ensure(lambda result: result is not None)
def read_journal(journal_id: int) -> Journal:
    return get_model(Journal, journal_id)


# Update a journal entry by its ID
@require(lambda journal_id: isinstance(journal_id, int))
@require(lambda dtstart: dtstart is None or isinstance(dtstart, datetime))
@require(lambda summary: summary is None or isinstance(summary, str))
@require(lambda description: description is None or isinstance(description, str))
@require(lambda calendar_id: calendar_id is None or isinstance(calendar_id, int))
@ensure(lambda result: result is not None)
def update_journal(
    journal_id: int,
    dtstart: datetime = None,
    summary: str = None,
    description: str = None,
    calendar_id: int = None,
) -> Journal:
    with update_model(Journal, journal_id) as journal:
        journal.dtstamp = datetime.utcnow()
        if dtstart is not None:
            journal.dtstart = dtstart
        if summary is not None:
            journal.summary = summary
        if description is not None:
            journal.description = description
        if calendar_id is not None:
            journal.calendar_id = calendar_id

        return journal


# Delete a journal entry by its ID
@require(lambda journal_id: isinstance(journal_id, int))
@ensure(lambda result: result is None)
def delete_journal(journal_id: int) -> None:
    delete_model(Journal, journal_id)


# List all journal entries
@require(lambda session: isinstance(session, Session))
@ensure(lambda result: isinstance(result, list))
def list_journals(session: Session) -> List[Journal]:
    journals = session.query(Journal).all()
    return journals
