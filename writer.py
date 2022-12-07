import csv
import os.path
import time
from pathlib import Path
from datetime import datetime


def write_data_to_csv(filepath: str, data: list[tuple] | list[list], header: list | tuple = None):
    dirname = os.path.dirname(filepath)
    Path(dirname).mkdir(parents=True, exist_ok=True)

    if len(data) <= 0:
        return

    with open(filepath, "w", encoding="UTF8") as f:
        # create CSV writer
        writer = csv.writer(f)

        # write CSV headers to the file
        if header is not None:
            writer.writerow(header)

        # write all the rows to the CSV file
        writer.writerows(data)


def write_data_to_cwd(filename: str, data: list[tuple] | list[list], header: list | tuple = None):
    cwd = os.getcwd()
    filepath = os.path.join(cwd, filename)
    write_data_to_csv(filepath, data, header)


def write_data_to_report_folder(filename: str, data: list[tuple] | list[list], header: list | tuple = None):
    cwd = os.getcwd()
    date_folder = generate_date_folder_name()
    filepath = os.path.join(cwd, "reports", date_folder, filename)
    write_data_to_csv(filepath, data, header)


def generate_date_folder_name() -> str:
    now = datetime.now()
    # create a string that represents the current date and time in the format:
    # YYYY-MM-DD_HH-MM (year-month-day_hour-minute-second)
    return now.strftime("%Y-%m-%d_%H-%M")
