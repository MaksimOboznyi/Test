from pathlib import Path

from pypdf import PdfReader

from utils.additional_info import build_additional_info
from utils.row_factory import create_empty_csv_row
from utils.text import clean_value


PDF_FIELDS = [
    "name",
    "date",
    "nationality",
    "address",
    "tel",
    "email",
]


PDF_ADDITIONAL_FIELDS = {
    "nationality": "NATIONALITY",
}


def read_pdf_text(file_path):
    reader = PdfReader(file_path)

    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_parts.append(page_text)

    return "\n".join(text_parts)


def parse_pdf_records(text):
    records = []
    current_record = {}
    pending_field = None

    for line in text.splitlines():
        line = line.strip()

        if not line or line == "Field Data":
            continue

        field = None
        value = None

        if line in PDF_FIELDS:
            pending_field = line
            continue

        if pending_field:
            field = pending_field
            value = line
            pending_field = None
        else:
            for pdf_field in PDF_FIELDS:
                prefix = f"{pdf_field} "

                if line.startswith(prefix):
                    field = pdf_field
                    value = line[len(prefix):].strip()
                    break

        if field is None:
            continue

        if field == "name" and current_record:
            if len(current_record) == len(PDF_FIELDS):
                records.append(current_record)

            current_record = {}

        current_record[field] = value

    if current_record and len(current_record) == len(PDF_FIELDS):
        records.append(current_record)

    return records


def convert_pdf_row_to_csv_row(pdf_row):
    result_row = create_empty_csv_row()

    name = clean_value(pdf_row.get("name"))

    result_row["name"] = name
    result_row["user_fullname"] = name
    result_row["usermail"] = clean_value(pdf_row.get("email"))
    result_row["address"] = clean_value(pdf_row.get("address"))
    result_row["tel"] = clean_value(pdf_row.get("tel"))
    result_row["dob"] = clean_value(pdf_row.get("date"))
    result_row["type"] = "pdf"

    result_row["user_additional_info"] = build_additional_info(
        pdf_row,
        PDF_ADDITIONAL_FIELDS,
    )

    return result_row


def parse_pdf(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    text = read_pdf_text(file_path)
    pdf_records = parse_pdf_records(text)

    parsed_rows = []

    for pdf_row in pdf_records:
        result_row = convert_pdf_row_to_csv_row(pdf_row)
        parsed_rows.append(result_row)

    return parsed_rows