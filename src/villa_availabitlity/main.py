from src.villa_availabitlity.common import print_availability_results
from src.villa_availabitlity.nmb import scrape_nmb
from src.villa_availabitlity.intervillas import scrape_intervillas


if __name__ == "__main__":
    print('--- Analyzing NMB ---')
    villas = scrape_nmb()
    print_availability_results(villas)

    print('--- Analyzing Intervillas ---')
    intervillas = scrape_intervillas()
    print_availability_results(intervillas)
