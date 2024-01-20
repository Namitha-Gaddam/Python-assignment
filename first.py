import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime, timedelta

def authenticate_gspread():
    # Load credentials from the JSON file provided by Google API Console
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('https://docs.google.com/spreadsheets/d/1VwEbwH-UWAKRqD-34esuqyjIpgCvwGgk/edit#gid=478598190', scope)
    client = gspread.authorize(creds)
    return client

def analyze_google_sheets(https://docs.google.com/spreadsheets/d/1eRujNQYov-tZ8j9yvkah6lSzJOpNweMF/edit?usp=sharing&ouid=112202623045573667171&rtpof=true&sd=true):
    client = authenticate_gspread()

    # Open the Google Sheets document
    sheet = client.open_by_url(https://docs.google.com/spreadsheets/d/1eRujNQYov-tZ8j9yvkah6lSzJOpNweMF/edit?usp=sharing&ouid=112202623045573667171&rtpof=true&sd=true)
    worksheet = sheet.get_worksheet(0)  # assuming data is in the first sheet

    # Get all values from the sheet
    values = worksheet.get_all_values()

    # Convert the data to a pandas DataFrame for easier manipulation
    df = pd.DataFrame(values[1:], columns=values[0])

    for i in range(len(df) - 1):
        start_time1 = datetime.strptime(df['Start Time'][i], "%H:%M")
        end_time1 = datetime.strptime(df['End Time'][i], "%H:%M")

        start_time2 = datetime.strptime(df['Start Time'][i + 1], "%H:%M")
        end_time2 = datetime.strptime(df['End Time'][i + 1], "%H:%M")

        # a) Worked for 7 consecutive days
        if (end_time1 + timedelta(days=1)) == start_time2:
            print(f"{df['Name'][i]} ({df['Position'][i]}) has worked for 7 consecutive days.")

        # b) Less than 10 hours between shifts but greater than 1 hour
        time_between_shifts = start_time2 - end_time1
        if timedelta(hours=1) < time_between_shifts < timedelta(hours=10):
            print(f"{df['Name'][i]} ({df['Position'][i]}) and {df['Name'][i + 1]} ({df['Position'][i + 1]}) have less than 10 hours between shifts but more than 1 hour.")

        # c) Worked for more than 14 hours in a single shift
        if (end_time1 - start_time1) > timedelta(hours=14):
            print(f"{df['Name'][i]} ({df['Position'][i]}) has worked for more than 14 hours in a single shift.")

