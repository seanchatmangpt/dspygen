import time

from dspygen.pyautomator.event_kit.reminder import Reminder
from dspygen.utils.dspy_tools import init_dspy
from dspygen.modules.comment_module import comment_call

def update_message(reminder):
    """Update the message based on the current notes using comment_call"""
    print(f"Updating message for reminder: {reminder.ci_id}")
    # Assuming the reminder's title is stored in a 'title' attribute
    # If not, you may need to adjust this part
    updated_message = comment_call(vid_title=reminder.title, words=reminder.notes)
    reminder.notes = updated_message
    reminder.save()



def main():
    """Main function"""
    init_dspy()

    wintermute = Reminder.from_id(reminder_id="AACB789A-9234-4216-94D9-626DDBF25A02")
    print(wintermute)

    update_message(wintermute)


if __name__ == '__main__':
    main()
