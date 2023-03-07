from bs4 import BeautifulSoup
from datetime import datetime
import requests


def get_menus(restaurant):
    r_number = {'R1': 13, 'R2': 21}
    url = 'https://novae-restauration.ch/menus/menu-week/cern/' + \
         f'{r_number[restaurant]}'

    # Get the page
    r = requests.get(url)
    text = r.text
    soup = BeautifulSoup(text, 'html.parser')

    # Only get the menu for the current day
    current_day = datetime.now().strftime('%-d')
    days = soup.findAll("h2", {"class": "nzg-menu-day-title text-center"})
    current = [d for d in days if current_day in d.text]
    print(current)
    current=current[0]
    
    # Get the div of the menu itself
    menus = current.parent.div
    res = []
    for menu in menus.findChildren(recursive=False):
        menu_name = menu.h4.text
        menu_price = menu.span.text
        menu_plate = menu.p.text

        res.append({'name': menu_name, 
                    'plate': menu_plate, 
                    'price': menu_price})
    return res


def pretty_print_menus(menus):
    txt = ""
    txt += '==== Menu for today ==== \n\n'
    for menu in menus:
        txt += f'--- {menu["name"]} ({menu["price"]}) ---\n'
        txt += f'  {menu["plate"]}\n\n'

    print(txt)
    return txt


if __name__ == "__main__":
    menus = get_menus(restaurant='R2')
    pretty_print_menus(menus)