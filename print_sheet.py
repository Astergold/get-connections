import gspread
from google.oauth2.service_account import Credentials
from main import *
json_key_file = 'aster-sheet-key.json'
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(json_key_file, scopes=scope)
client = gspread.authorize(creds)
spreadsheet = client.open("Linkedin-connections")
account1_sheet = spreadsheet.worksheet("sheet1")
account1_data = account1_sheet.get_all_values()
for row in account1_data:
    print(row)
