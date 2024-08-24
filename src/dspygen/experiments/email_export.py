import os
import pandas as pd
import subprocess

def main():
    # AppleScript to fetch emails from the Mail app
    apple_script = """
    tell application "Mail"
        set emailList to {}
        set theMessages to messages of inbox
        repeat with eachMessage in theMessages
            set emailSubject to subject of eachMessage
            set emailSender to sender of eachMessage
            set emailRecipient to (address of every recipient of eachMessage as string)
            set emailDateReceived to date received of eachMessage
            set emailContent to content of eachMessage
            set end of emailList to emailSubject & tab & emailSender & tab & emailRecipient & tab & emailDateReceived & tab & emailContent
        end repeat
    end tell
    return emailList as string
    """

    # Run the AppleScript
    process = subprocess.Popen(['osascript', '-e', apple_script], stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(f"Error: {error}")
        return

    # Convert the output to a readable format
    email_data = output.decode('utf-8').split('\n')

    # Split the tab-separated values into a list of dictionaries
    email_list = [
        {
            "Subject": item.split('\t')[0],
            "From": item.split('\t')[1],
            "To": item.split('\t')[2],
            "Date": item.split('\t')[3],
            "Body": item.split('\t')[4],
        }
        for item in email_data if item
    ]

    # Create a DataFrame and save it as CSV
    df = pd.DataFrame(email_list)
    df.to_csv("emails.csv", index=False)

    print("Emails have been saved to emails.csv")

if __name__ == "__main__":
    main()
