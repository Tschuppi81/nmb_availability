from datetime import datetime

from src.villa_availabitlity.common import print_availability_results, \
    draw_availability_graph, store_villa_data, load_villa_data
from src.villa_availabitlity.intervillas import scrape_intervillas
from src.villa_availabitlity.nmb import scrape_nmb
from src.villa_availabitlity.t_menu import Menu

today = datetime.today().strftime('%Y%m%d')


def scrape_and_store_data():
    print('--- Scraping data ---')
    print('- NMB')
    villas = scrape_nmb()
    store_villa_data(villas, 'nmb')

    print('- Intervillas')
    intervillas = scrape_intervillas()
    store_villa_data(intervillas, 'intervillas')


def load_and_show_data():
    print('--- Show NMB data ---')
    villas = load_villa_data('nmb')
    print_availability_results(villas)
    draw_availability_graph(villas, f'../../plots/{today}_nmb.png')

    print('--- Show Intervilla data ---')
    intervillas = load_villa_data('intervillas')
    print_availability_results(intervillas)
    draw_availability_graph(intervillas, f'../../plots/{today}_intervillas.png')


if __name__ == "__main__":
    menu = Menu(0, 'Villa availability')
    menu.add_sub_menu(Menu(1, 'Scrape webpages and store data', scrape_and_store_data))
    menu.add_sub_menu(Menu(2, 'Load data and visualize it', load_and_show_data))

    menu.run()

