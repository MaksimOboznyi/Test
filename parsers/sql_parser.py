import ast
from pathlib import Path

from utils.additional_info import build_additional_info
from utils.row_factory import create_empty_csv_row
from utils.text import clean_value


SQL_COLUMNS = [
    "userid",
    "name",
    "username",
    "password",
    "email",
    "permission",
    "sex",
    "country",
    "birth",
]


SQL_ADDITIONAL_FIELDS = {
    "sex": "SEX",
}


def parse_sql_line(line):
    line = line.strip()

    if not line.startswith("("):
        return None

    if line.endswith(","):
        line = line[:-1]

    if line.endswith(";"):
        line = line[:-1]

    try:
        values = ast.literal_eval(line)
    except (SyntaxError, ValueError):
        return None

    if len(values) != len(SQL_COLUMNS):
        return None

    return dict(zip(SQL_COLUMNS, values))


def convert_sql_row_to_csv_row(sql_row):
    result_row = create_empty_csv_row()

    result_row["user_ID"] = clean_value(sql_row.get("userid"))
    result_row["name"] = clean_value(sql_row.get("name"))
    result_row["username"] = clean_value(sql_row.get("username"))
    result_row["usermail"] = clean_value(sql_row.get("email"))
    result_row["country"] = clean_value(sql_row.get("country"))
    result_row["user_fullname"] = clean_value(sql_row.get("name"))
    result_row["type"] = "sql"

    birth = clean_value(sql_row.get("birth"))
    if birth != "0":
        result_row["dob"] = birth

    result_row["user_additional_info"] = build_additional_info(
        sql_row,
        SQL_ADDITIONAL_FIELDS,
    )

    return result_row


def parse_sql(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"SQL file not found: {file_path}")

    parsed_rows = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            sql_row = parse_sql_line(line)

            if sql_row is None:
                continue

            result_row = convert_sql_row_to_csv_row(sql_row)
            parsed_rows.append(result_row)

    return parsed_rows