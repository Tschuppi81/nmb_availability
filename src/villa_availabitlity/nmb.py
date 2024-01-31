import requests

from bs4 import BeautifulSoup

from src.villa_availabitlity.common import get_month_days, \
    calculate_percentage_blocked


def get_available_and_blocked_days(url):
    # Fetch HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    calendar_wrapper = soup.find(id='fwre-item-calendar-wrapper')
    for month in calendar_wrapper.find_all('table'):
        month_str = month.find('th').text
        total_days_month = get_month_days(month_str.split(' ')[1],
                                          month_str.split(' ')[0])
        booked_days_elements = month.find_all(class_='fwre-booking-active')
        checkin_days_elements = month.find_all(class_='checkin')
        checkout_days_elements = month.find_all(class_='checkout')
        available_days_elements = month.find_all('td', class_=None)
        blocked_days = (len(booked_days_elements) +
                        len(checkin_days_elements)) # +
                        # len(checkout_days_elements)

        yield month_str, blocked_days


def get_nmb_villas(url):
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

        # for testing
        if len(villas) > 5:
            break

    print(f'Found {len(villas)} villas')
    return villas


def scrape_nmb():
    url = "https://www.nmbfloridavacationrentals.com/all-vacation-rentals"
    villas = []
    for villa in get_nmb_villas(url):
        villa['months'] = []

        print(f'{villa["name"]}')
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

        villas.append(villa)

    return villas
