from datetime import datetime


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def format_date(date_str, input_format="%Y-%m-%d", output_format="%d-%m-%Y"):
    return datetime.strptime(date_str, input_format).strftime(output_format)
