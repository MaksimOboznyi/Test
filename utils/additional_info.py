from utils.text import clean_additional_info_value


def build_additional_info(source_row, fields_mapping):
    additional_info = []

    for source_field, output_label in fields_mapping.items():
        value = source_row.get(source_field)
        value = clean_additional_info_value(value)

        if value:
            additional_info.append(f"{output_label}: {value}")

    return "|".join(additional_info)