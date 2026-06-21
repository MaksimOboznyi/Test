def clean_value(value):
    if value is None:
        return ""

    return str(value).strip()


def clean_additional_info_value(value):
    value = clean_value(value)

    value = value.replace("\n", " ")
    value = value.replace("\r", " ")
    value = value.replace("|", "/")

    return value