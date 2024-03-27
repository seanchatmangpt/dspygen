from dspygen.experiments.rfc5545.ical_db_session import get_session
from dspygen.experiments.rfc5545.ical_models import Event


def create_event():
    Event.create(dtstart="2021-01-01T00:00:00", dtend="2021-01-01T01:00:00", summary="Test event")


def get_events():
    events = Event.get_by_page(page=0, per_page=10, include_past=True)
    for event in events:
        print(event)
    return events


def update_event():
    event = Event.update(event_id=1, summary="Updated event")


def main():
    """Main function"""
    get_session()
    # create_event()
    # get_events()
    update_event()
    get_events()

if __name__ == '__main__':
    main()
