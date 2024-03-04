import os.path

from src.villa_availabitlity.common import print_availability_results
from src.villa_availabitlity.intervillas import scrape_intervillas
from src.villa_availabitlity.nmb import scrape_nmb
from src.villa_availabitlity.utils import load_villa_data, store_villa_data

if __name__ == "__main__":
    print('Loading data from file')
    path = os.path.join(os.path.dirname(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir, os.pardir))
    path = os.path.join(path, 'data', 'villa_data.json')
    villas = load_villa_data(path)

    print('--- Analyzing NMB ---')
    nmb = scrape_nmb()
    print_availability_results(villas)
    villas = merge_villas(villas, nmb)

    print('--- Analyzing Intervillas ---')
    intervillas = scrape_intervillas()
    print_availability_results(intervillas)
    villas = merge_villas(villas, intervillas)

    print('Storing data to file')
    store_villa_data('villa_data.json', villas)
