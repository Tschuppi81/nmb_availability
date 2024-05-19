from datetime import datetime

from src.villa_availabitlity.common import print_availability_results, \
    draw_availability_graph, store_villa_data, load_villa_data
from src.villa_availabitlity.intervillas import scrape_intervillas
from src.villa_availabitlity.nmb import scrape_nmb


if __name__ == "__main__":
    today = datetime.today().strftime('%Y%m%d')

    # menu scrape and store data
    # menu load and show data

    print('--- Analyzing NMB ---')
    # villas = scrape_nmb()
    # store_villa_data(villas, 'nmb')

    villas = load_villa_data('nmb')
    print_availability_results(villas)
    draw_availability_graph(villas, f'../../plots/{today}_nmb.png')

    print('--- Analyzing Intervillas ---')
    # intervillas = scrape_intervillas()
    # store_villa_data(intervillas, 'intervillas')

    intervillas = load_villa_data('intervillas')
    print_availability_results(intervillas)
    draw_availability_graph(intervillas, f'../../plots/{today}_intervillas.png')
