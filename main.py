from pathlib import Path

from parsers.excel_parser import parse_excel
from parsers.sql_parser import parse_sql
from parsers.pdf_parser import parse_pdf


TASK_DIR = Path("task")

EXCEL_FILE_PATH = TASK_DIR / "excel" / "data.xlsx"
SQL_FILE_PATH = TASK_DIR / "sql" / "data.sql"
PDF_FILE_PATH = TASK_DIR / "pdf" / "data_pdf.pdf"


def main():
    excel_rows = parse_excel(EXCEL_FILE_PATH)
    sql_rows = parse_sql(SQL_FILE_PATH)
    pdf_rows = parse_pdf(PDF_FILE_PATH)

    all_rows = []
    all_rows.extend(excel_rows)
    all_rows.extend(sql_rows)
    all_rows.extend(pdf_rows)

    print(f"Excel rows: {len(excel_rows)}")
    print(f"SQL rows: {len(sql_rows)}")
    print(f"PDF rows: {len(pdf_rows)}")
    print(f"Total rows: {len(all_rows)}")


if __name__ == "__main__":
    main()