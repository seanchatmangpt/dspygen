import inject
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

from dspygen.utils.file_tools import project_dir


def configure(binder):
    """Configure dependency injection bindings."""

    credentials_json = project_dir() / "credentials.json"

    if not Path(credentials_json).exists():
        return

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(credentials_json, scopes=scopes)
    client = gspread.authorize(creds)

    binder.bind(Credentials, creds)
    binder.bind(gspread.Client, client)
