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

def scrape_site():
    '''
    Scrapes rpi_url; run_spinster and found_one are 
    reset at the start of every instance of this function. Spoofs Safari 
    15.1 (17612.2.9.1.20) on MacOS Monterey 12.0.1.
    '''
    global run_spinster
    run_spinster = True
    found_one = False
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
        table = soup.find(id='myTable')
        
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if "Yes" in cells[4]:
                    urls = row.find_all('a')
                    url = urls[0]['href']
                    price = urls[1].text
                    model = cells[0].text
                    store = cells[3].text
                    print("\n[" + time.strftime("%Y%m%d %H:%M:%S") + "] Found " + model + " at " + store + " / " + url + " for " + price)
                    found_one = True

            if found_one == False:    
                print("\n[" + time.strftime("%Y%m%d %H:%M:%S") + "] Nothing's in stock. Chip shortage is still a thing.")
        else:
            print("\n[" + time.strftime("%Y%m%d %H:%M:%S") + "] Raspberry Pi table not found on page; aborting.")
    
    else:
        print("\n[" + time.strftime("%Y%m%d %H:%M:%S") + "] Page returned status code " + str(pi4_page.status_code))


if __name__ == "__main__":
    # Arg parser
    version = "version 2022.02.08.000"
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
            for i in tqdm(range(interval), total = None, desc = "Time until next run"):
                time.sleep(1)
    else:
        scrape_site()
