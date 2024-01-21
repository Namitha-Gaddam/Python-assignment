import pandas as pd

def analyze_excel_file(file_path):
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path, sheet_name='Sheet1')

    # Sort the DataFrame by 'Name' and 'Date'
    df.sort_values(by=['Name', 'Date'], inplace=True)

    # Reset the index after sorting
    df.reset_index(drop=True, inplace=True)

    # Function to check consecutive days worked
    def consecutive_days_worked(row):
        return all(df.loc[i, 'Date'] - df.loc[i - 1, 'Date'] == pd.Timedelta(days=1) for i in range(1, len(df)))

    # Function to check time between shifts
    def time_between_shifts(row):
        return (row['Date'] - df.loc[row.name - 1, 'Date']).seconds / 3600 < 10 and \
               (row['Date'] - df.loc[row.name - 1, 'Date']).seconds / 3600 > 1

    # Function to check hours worked in a single shift
    def hours_in_single_shift(row):
        return row['Hours Worked'] > 14

    # Apply the functions to create boolean masks
    consecutive_mask = df.groupby('Name').apply(consecutive_days_worked).reset_index(level=0, drop=True)
    time_between_shifts_mask = df.apply(time_between_shifts, axis=1)
    hours_in_single_shift_mask = df.apply(hours_in_single_shift, axis=1)

    # Print the results
    print("Employees who have worked for 7 consecutive days:")
    print(df[consecutive_mask][['Name', 'Position']])

    print("\nEmployees who have less than 10 hours of time between shifts but greater than 1 hour:")
    print(df[time_between_shifts_mask][['Name', 'Position']])

    print("\nEmployees who have worked for more than 14 hours in a single shift:")
    print(df[hours_in_single_shift_mask][['Name', 'Position']])

# Example usage
file_path = r"C:\Users\namit\OneDrive\Desktop\Data.xlsx"
analyze_excel_file(file_path)
       
