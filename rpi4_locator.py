#!/usr/bin/env python3

import traceback
import argparse
import threading
import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from progress.spinner import MoonSpinner

def spinster():
    'Run a spinner thread. Ghetto use of global "run_spinster" to end thread.'
    spinner = MoonSpinner("[" + time.strftime("%Y%m%d %H:%M:%S") + "] Grabbing " + rpi_url + "… ")
    while run_spinster:
        spinner.next()
        time.sleep(0.1)
    print("\n")

def scrape_site():
    '''
    Scrapes rpi_url; run_spinster is reset at the start of every instance
    of this function. Spoofs Safari 15.1 (17612.2.9.1.20) on MacOS Monterey 
    12.0.1.
    '''
    global run_spinster
    run_spinster = True
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'
    }

    spinner = threading.Thread(target=spinster)
    spinner.start()
    pi4_page = requests.get(rpi_url, headers=headers, timeout = 10)
    run_spinster = False
    spinner.join()
    
    if pi4_page.status_code == 200:    
        soup = BeautifulSoup(pi4_page.text, 'html.parser')
        found_cells = soup.find_all("td", string="Yes")
        
        if found_cells:
            for cell in found_cells:
                cells = cell.find_previous_siblings("td")
                found_data = {
                    'store': cells[0].text,
                    'model': cells[3].text,
                    'price': cell.find_next_siblings("td")
                }
                found_data['url'] = found_data['price'][1].find('a')['href']
                found_data['price'] =  found_data['price'][1].find('a').text
                notify(found_data)
        else:
            print("[" + time.strftime("%Y%m%d %H:%M:%S") + "] Nothing's in stock. Chip shortage is still a thing.")
    else:
        print("[" + time.strftime("%Y%m%d %H:%M:%S") + "] Page returned status code " + str(pi4_page.status_code))

def notify(f_data):
    '''
    f_data is a dictionary with keys store, model, price, and url of an in 
    stock Raspberry Pi. Broken out into a function for easier notification
    expansions as necessary.
    '''
    print("[" + time.strftime("%Y%m%d %H:%M:%S") + "] Found " + f_data['model'] + " at " + f_data['store'] + " / " + f_data['url'] + " for " + f_data['price'])

if __name__ == "__main__":
    # Arg parser
    version = "version 2022.02.22.002"
    helptext = """
        Checks https://rpilocator.com for any available Raspberry Pi 4 Model Bs

        """
    epilog_str = """
        """ + version
    parser = argparse.ArgumentParser(description = helptext, epilog = epilog_str)
    parser.add_argument("-n", "--not-continuous", default = False, 
        action = 'store_true', help = "Run once and exit.")
    parser.add_argument("-i", "--interval", metavar = "seconds", type = int,
        default = 1800, 
        help = "If running continuously, time in seconds between scraping the page. Do not recommend anything less than 30 minutes.")
    parser.add_argument("-u", "--usa-usa", default = False,
        action = 'store_true', 
        help = "Check US locations only. USA! USA! Note that this will search all available devices, not just Raspberry Pi 4s. There is no way to restrict searches by multiple criteria.")
    args = parser.parse_args()

    continuous = not args.not_continuous
    interval = args.interval
    
    if args.usa_usa:
        rpi_url = 'https://rpilocator.com/?country=US'
    else:
        rpi_url = 'https://rpilocator.com/?cat=PI4'
    
    if continuous:
        while True:
            scrape_site()
            for i in tqdm(range(interval), total = None, desc = "[" + time.strftime("%Y%m%d %H:%M:%S") + "] Time until next run"):
                time.sleep(1)
    else:
        scrape_site()
