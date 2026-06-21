from parsers.excel_parser import parse_excel
from pprint import pprint

def main():
    excel_rows = parse_excel("task/excel/data.xlsx")
    
    print(f"Строк из Excel: {len(excel_rows)}")

    for row in excel_rows[:3]:
        pprint(row, sort_dicts=None)


if __name__ == "__main__":
    main()
