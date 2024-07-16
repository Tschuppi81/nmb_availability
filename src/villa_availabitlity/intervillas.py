import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.villa_availabitlity.common import get_month_days, \
    calculate_percentage_blocked

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(
    options=options, service=Service('/usr/bin/chromedriver'))


def get_intervillas(url) -> list[dict]:
    villas = []

    base_url, rel_url = url.rsplit('/', 1)

    # Fetch HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # find each villa
    for v in soup.find_all('div', class_='ident'):
        villa = {}
        villa['name'] = v.find('h4').text.strip()
        villa['url'] = base_url + v.find('a')['href']
        villas.append(villa)

        # for testing
        if len(villas) > 5:
            break

    print(f'Found {len(villas)} villas')
    return sorted(villas, key=lambda v: v['name'])


def get_available_and_blocked_days_intervillas(url) -> tuple[str, int]:
    month_str = ''

    # Navigate to the URL with JavaScript rendering
    driver.get(url)

    # Wait for some element to be present (loading time)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'date'))
    )

    for _ in range(6):  # for the next number of months
        # button next month
        button_next_month = driver.find_element(By.CLASS_NAME, 'ml-1')

        # Find selected month and year
        selected_month = driver.find_element(By.NAME, 'month')
        month = (Select(selected_month).first_selected_option.text.
                 replace('ä', 'a'))
        selected_year = driver.find_element(By.NAME, 'year')
        year = Select(selected_year).first_selected_option.text
        month_str = f'{month} {year}'

        # Find elements with the class 'date'
        date_elements = driver.find_elements(By.CLASS_NAME, 'date')
        date_elements = [date_element for date_element in date_elements if
                         date_element.text in [str(i) for i in range(1, 32)]]
        nbr_of_days = len(date_elements)

        nbr_of_full_days_blocked = len(driver.find_elements(
            By.CLASS_NAME, 'blocked-am.blocked-pm'))
        nbr_of_checkins = len(driver.find_elements(
            By.CLASS_NAME, 'free.blocked-am'))
        nbr_of_checkouts = len(driver.find_elements(
            By.CLASS_NAME, 'free.blocked-pm'))
        nbr_of_full_days_available = (nbr_of_days - nbr_of_full_days_blocked -
                                      nbr_of_checkins - nbr_of_checkouts)

        yield month_str, nbr_of_full_days_blocked + nbr_of_checkins
        button_next_month.click()


def scrape_intervillas() -> list[dict]:
    url = "https://www.intervillas-florida.com/ferienhaus-cape-coral"
    intervillas = []
    for villa in get_intervillas(url):
        villa['months'] = []

        print(f'{villa["name"]}')
        for month_str, blocked_days in (
                get_available_and_blocked_days_intervillas(villa['url'])):
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

        # calculate average percentage blocked
        villa['average_percentage_blocked'] = sum(
            [month['percentage_blocked'] for month in villa['months']]) / len(
            villa['months'])

        intervillas.append(villa)

    return intervillas
