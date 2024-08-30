from datetime import datetime, timedelta
import logging

from dspygen.pyautomator.calendar.calendar_app import CalendarApp
from dspygen.utils.dspy_tools import init_dspy

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def eval_create_event():
    app = CalendarApp()
    app.request_access()

    event_prompt = (
        "Schedule a team meeting titled 'Quarterly Project Review' for next Saturday at 2 PM for 1.5 hours. "
        "The topic is 'Project Review and Planning'. Location: Conference Room A. "
        "Attendees: Alice Smith (alice@example.com), Bob Johnson (bob@example.com). "
        "Organizer: David Miller (david@example.com). "
        "Please add a reminder 15 minutes before the event."
    )
    try:
        result = app.create_event_from_generated(event_prompt)
        logger.info(result)
        logger.info("Please add this event manually to your calendar using the generated iCalendar data.")
    except Exception as e:
        logger.error(f"Error generating event data: {e}")


def eval_get_events():
    app = CalendarApp()
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    events = app.get_events(start_date, end_date)
    logger.info(f"Events in the next week: {len(events)}")
    for event in events:
        logger.info(f"- {event['title']} on {event['start_date']}")


def eval_text_query():
    app = CalendarApp()
    app.request_access()

    queries = [
        "Find all meetings scheduled for next week",
        "Show me events with 'Project' in the title",
        "List events happening in Conference Room A",
        "Find events organized by David Miller",
        "Show me events with more than 3 attendees"
    ]

    for query in queries:
        logger.info(f"\nExecuting query: '{query}'")
        results = app.text_query(query)
        logger.info(f"Found {len(results)} events:")
        for event in results:
            logger.info(f"- {event['title']} on {event['start_date']} at {event['location']}")

def main():
    init_dspy()

    logger.info("Evaluating event creation:")
    # eval_create_event()

    logger.info("\nEvaluating event retrieval:")
    # eval_get_events()

    logger.info("\nEvaluating text query:")
    eval_text_query()


if __name__ == "__main__":
    main()
