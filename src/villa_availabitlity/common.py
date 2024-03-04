import calendar
from typing import Union


def get_month_days(year: Union[int, str], month: Union[int, str]) -> int:
    month_map = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'mai': 5,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12,
    }
    if isinstance(month, str):
        if month.isdigit():
            month = int(month)
        month = month_map[month[:3].lower()]
    if isinstance(year, str):
        year = int(year)
    _, last_day = calendar.monthrange(year, month)
    return last_day


def get_month_abbr(full_month_name: str) -> str:
    """
    This function takes a full month name as a string and returns its
    abbreviation.

    full_month_name (str): The full name of the month (e.g., 'January').
    Returns str: The abbreviated name of the month (e.g., 'Jan').
    """
    month_number = list(calendar.month_name).index(full_month_name.capitalize())
    return calendar.month_abbr[month_number]


def calculate_percentage_blocked(blocked_days: int, total_days: int) -> float:
    return (blocked_days / total_days) * 100


def print_availability_results(villas: list[dict]) -> None:
    """
    Print the availability results. The format is like the following:
    #            | month 1 | month 2 | ..
    # villa  1   |         |         | ..
    # villa  2   |         |         | ..
    # ..         |         |         | ..
    """

    # Get unique months
    unique_months = list()
    for villa in villas:
        for month in villa["months"]:
            unique_months.append(month["month_name"])
        break

    # Print the header
    header = "| {:<30} |".format('Villa')
    sep_line = "+ {:<30} +".format('-' * 30)
    for month in unique_months:
        header += " {:>8} |".format(month)
        sep_line += " {:>8} +".format('-' * 8)
    header += " {:>8} |".format('Average')
    sep_line += " {:>8} +".format('-' * 8)

    print(sep_line)
    print(header)
    print(sep_line)

    # Print villa blocked days for each month
    for villa in villas:
        villa_line = "| {:<30} |".format(villa["name"][:30])
        for month in unique_months:
            for data in villa["months"]:
                if data["month_name"] == month:
                    if 'percentage_blocked' in data:
                        val = round(data["percentage_blocked"], 1)
                        villa_line += " {:>14.1f} |".format(val)
                    else:
                        villa_line += " {:>14} |".format('-')
                    break
            else:
                # month is not present
                villa_line += " {:>14} |".format('+')  # If data for the
        # print average percentage blocked for the villa
        villa_line += " {:>14.1f} |".format(villa["average_percentage_blocked"])
        print(villa_line)

    print(sep_line)


