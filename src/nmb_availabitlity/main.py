import calendar
import requests

from bs4 import BeautifulSoup

# css classes for booking state
booked = 'fwre-booking-active'
checkin = 'checkin'
checkout = 'checkout'


# available = no class


def get_month_days(year, month):
    month_map = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
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


def calculate_percentage_blocked(blocked_days, total_days):
    return (len(blocked_days) / total_days) * 100


def get_available_and_blocked_days(url):
    # Fetch HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    calendar_wrapper = soup.find(id='fwre-item-calendar-wrapper')
    for month in calendar_wrapper.find_all('table'):
        month_str = month.find('th').text
        booked_days_elements = month.find_all(class_=booked)
        checkin_days_elements = month.find_all(class_=checkin)
        checkout_days_elements = month.find_all(class_=checkout)
        blocked_days = (len(booked_days_elements) +
                        len(checkin_days_elements) +
                        len(checkout_days_elements))

        yield month_str, blocked_days


def calculate_percentage_blocked(blocked_days, total_days):
    return (blocked_days / total_days) * 100


def get_villas(url):
    villas = []

    base_url, rel_url = url.rsplit('/', 1)

    # Fetch HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # find each villa
    for v in soup.find_all('div', class_='fw-list-property'):
        villa = {}
        villa['name'] = v.find('h2').text.strip()
        villa['url'] = base_url + v.find('a')['href']
        villas.append(villa)

    print(f'Found {len(villas)} villas')
    return villas


def print_availablitly_results(villas):
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
        header += " {:>14} |".format(month)
        sep_line += " {:>14} +".format('-' * 14)

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
        print(villa_line)

    print(sep_line)


if __name__ == "__main__":
    villas = []

    url = ("https://www.nmbfloridavacationrentals.com/all-vacation-rentals")
    for villa in get_villas(url):
        villa['months'] = []

        print(f'\n{villa["name"]}')
        for month_str, blocked_days in (
                get_available_and_blocked_days(villa['url'])):
            total_days_month = get_month_days(month_str.split(' ')[1],
                                              month_str.split(' ')[0])
            available_days = total_days_month - blocked_days
            percentage_blocked = calculate_percentage_blocked(blocked_days,
                                                              total_days_month)
            month = {
                'month_name': month_str,
                'available_days': available_days,
                'blocked_days': blocked_days,
                'percentage_blocked': percentage_blocked
            }
            villa['months'].append(month)
            print(f'  {month_str}')
            print(f'    Booked: {blocked_days}')
            print(f'    Available: {available_days}')
            print(f'    Percentage of Blocked Days: {percentage_blocked:.2f}%')

        villas.append(villa)

    print_availablitly_results(villas)
