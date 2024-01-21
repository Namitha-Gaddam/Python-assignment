import csv
from datetime import datetime, timedelta
import openpyxl

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

def analyze_file(file_path):
    # Open the CSV file and read the data
    with open(file_path, 'r') as file:
        reader = openpyxl.DictReader(file)
        
        # Create a dictionary to store employees' data
        employees = {}

        # Loop through each row in the CSV
        for row in reader:
            name = row['Name']
            position = row['Position']
            date = parse_date(row['Date'])
            hours_worked = float(row['Hours Worked'])

            # Check for employees who worked for 7 consecutive days
            if name in employees:
                if (date - employees[name]['last_date']).days == 1:
                    employees[name]['consecutive_days'] += 1
                else:
                    employees[name]['consecutive_days'] = 1
            else:
                employees[name] = {'consecutive_days': 1, 'last_date': date}

            # Check for employees with less than 10 hours between shifts but greater than 1 hour
            if 'last_shift_end' in employees[name]:
                time_between_shifts = date - employees[name]['last_shift_end']
                if 1 < time_between_shifts.total_seconds() // 3600 < 10:
                    print(f"{name} ({position}) has less than 10 hours between shifts on {date}")

            employees[name]['last_shift_end'] = date + timedelta(hours=hours_worked)


            # Check for employees who worked for more than 14 hours in a single shift
            if hours_worked > 14:
                print(f"{name} ({position}) worked for more than 14 hours in a single shift.")
    # Print employees who worked for 7 consecutive days
    if consecutive_days == 7:
        print(f"{name} ({position}) worked for 7 consecutive days.")
    for name, data in employees.items():
        if data['consecutive_days'] == 7:
            print(f"{name} ({data['last_date'].strftime('%Y-%m-%d')} to {data['last_date'] + timedelta(days=6)}): Worked for 7 consecutive days")

# Assuming the input CSV file has headers: "Name", "Position", "Date", "Hours Worked"
input_file_path = '/content/Assignment_Timecard.xlsx'
analyze_file(input_file_path)

   
