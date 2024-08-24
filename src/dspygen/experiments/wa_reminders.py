import csv
import subprocess
import typer
from typing import Optional, List
import pyperclip
import io
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime, date

app = typer.Typer()

class Reminder(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    notes: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[date] = None

    @classmethod
    def from_row(cls, row: dict) -> 'Reminder':
        due_date = None
        if row.get('due_date'):
            try:
                due_date = datetime.strptime(row['due_date'], "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Invalid date format for due_date: {row['due_date']}. Expected format: YYYY-MM-DD")
        
        return cls(
            title=row['title'],
            notes=row.get('notes'),
            due_date=due_date
        )

def run_applescript(script: str) -> None:
    process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        typer.echo(f"Error: {error.decode('utf-8')}", err=True)
    else:
        typer.echo("Reminder added successfully.")

def create_reminder(reminder: Reminder, list_name: Optional[str] = None) -> None:
    script = f'''
    tell application "Reminders"
        set newReminder to make new reminder
        set name of newReminder to "{reminder.title.replace('"', '\\"')}"
    '''

    if reminder.notes:
        script += f'set body of newReminder to "{reminder.notes.replace('"', '\\"')}"\n'

    if reminder.due_date:
        script += f'set due date of newReminder to date "{reminder.due_date.isoformat()}"\n'

    if list_name:
        script += f'''
        set targetList to list "{list_name}"
        if exists targetList then
            move newReminder to targetList
        else
            set newList to make new list with properties {{name:"{list_name}"}}
            move newReminder to newList
        end if
        '''
    
    script += 'end tell'
    
    run_applescript(script)

def process_csv_data(csv_data: str, list_name: Optional[str] = None) -> List[Reminder]:
    reader = csv.DictReader(io.StringIO(csv_data))
    reminders: List[Reminder] = []
    
    for row in reader:
        try:
            reminder = Reminder.from_row(row)
            reminders.append(reminder)
        except ValidationError as e:
            typer.echo(f"Error validating row: {e}", err=True)
            raise typer.Exit(code=1)
        except ValueError as e:
            typer.echo(f"Error validating row: {e}", err=True)
            raise typer.Exit(code=1)

    if not reminders:
        typer.echo("No valid reminders found in CSV data.", err=True)
        raise typer.Exit(code=1)

    for reminder in reminders:
        create_reminder(reminder, list_name)

    return reminders

def import_reminders_from_file(csv_file: str, list_name: Optional[str] = None) -> List[Reminder]:
    try:
        with open(csv_file, 'r') as file:
            csv_data = file.read()
        return process_csv_data(csv_data, list_name)
    except FileNotFoundError:
        typer.echo(f"Error: CSV file '{csv_file}' not found.", err=True)
        raise typer.Exit(code=1)
    except csv.Error as e:
        typer.echo(f"Error reading CSV file: {e}", err=True)
        raise typer.Exit(code=1)

def import_reminders_from_clipboard(list_name: Optional[str] = None) -> List[Reminder]:
    try:
        csv_data = pyperclip.paste()
        return process_csv_data(csv_data, list_name)
    except csv.Error as e:
        typer.echo(f"Error reading CSV data from clipboard: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def import_reminders(
    csv_file: str = typer.Argument(..., help="Path to the CSV file containing reminders"),
    list_name: Optional[str] = typer.Option(None, help="Name of the Reminders list to add to")
):
    """
    Import reminders from a CSV file into Apple's Reminders app.
    """
    reminders = import_reminders_from_file(csv_file, list_name)
    typer.echo(f"Successfully imported {len(reminders)} reminders.")

@app.command()
def import_from_clipboard(
    list_name: Optional[str] = typer.Option(None, help="Name of the Reminders list to add to")
):
    """
    Import reminders from CSV data in the clipboard into Apple's Reminders app.
    """
    reminders = import_reminders_from_clipboard(list_name)
    typer.echo(f"Successfully imported {len(reminders)} reminders from clipboard.")

if __name__ == "__main__":
    app()