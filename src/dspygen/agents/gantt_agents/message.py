import gspread
from google.oauth2.service_account import Credentials

import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os
load_dotenv()

from bs4 import BeautifulSoup
import requests

from openai import OpenAI

clientAI = OpenAI()

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "10aU_0JoXzHyfq4_YCMDMqdiJGuLAdwiAq9PSegI53YI"
workbook = client.open_by_key(sheet_id)
#sheet = client.open_by_key(sheet_id).sheet1


#value_list = sheet.row_values(1)
#print(value_list)
def ShowAllSheetData(sheet):
    all_data = sheet.get_all_values()
    for row in all_data:
        print(row)
def GetRowData(sheet, row_number):
    row_data = sheet.row_values(row_number)
    print(f"Data in row {row_number}: {row_data}")
    return row_data

def GetColumnData(sheet, column_number):
    column_data = sheet.col_values(column_number)
    print(f"Data in column {column_number}: {column_data}")
    return column_data
def AddNewRowData(sheet, data):
    sheet.append_row(data)
    #data must be entered like ["Alice", "30", "New York"]

def UpdateCell(sheet,row, column, value):
    sheet.update_cell(row, column, value)

def send_email(subject, body, to_email):
    from_email = os.getenv('EMAIL_ADDRESS')
    app_password = os.getenv('EMAIL_PASSWORD')
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, msg.as_string())
    print("Email Sent.   To:" + str(to_email) + "   From:" + str(from_email) + "   Subject:" + subject)
    #send_email("testEmailnew", "bodyofmessagenew", "davidcolaco3@gmail.com")

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.title.string
def CreateLogSheet(workbook):
    try:
        sheet_list = workbook.worksheets()
        sheet_names = [sheet.title for sheet in sheet_list]
        if "logsheet" not in sheet_names:
            workbook.add_worksheet(title="logsheet", rows="100", cols="20")
            print("Logsheet created successfully.")
        else:
            print("Logsheet exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
def sheetSetup():
    CreateLogSheet(workbook)
    print("set up successfull")

def send_message_to_chatGPT(message):
    completion = clientAI.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant"},
            {"role": "user", "content": message}
        ]
    )

    response_message = completion.choices[0].message.content
    return response_message.strip()
    # print(send_message_to_poetic_assistant("tell me a joke"))