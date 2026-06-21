from constants import CSV_COLUMNS


def create_empty_csv_row():
    return dict.fromkeys(CSV_COLUMNS, "")