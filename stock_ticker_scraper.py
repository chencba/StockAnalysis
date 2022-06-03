
import requests
from lxml import etree
import time
import numpy as np
import json

class StockTickerScraper:
    """Scrape the top 200 tickers of Energy Industry from Yahoo Finance."""
    def __init__(self, offset, url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; \
                                               Intel Mac OS X 10_13_3) AppleWebKit/537.36 \
                                               (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}, \
                                                   filename = "tickers_companynames.txt"):
        self.url = url
        self.headers = headers
        self.offset = offset
        self.filename = filename
        
    def get_one_page(self):
        """Download one page from a given url."""
        try:
            response = requests.get(self.url, headers = self.headers)
            if response.status_code == 200:
                return response.text
            return None
        except requests.RequestException:
            print("Fail")

    def parse_one_page(self, html):
        """Parse the page we download and find the extact contents we need."""
        html = etree.HTML(html)
        path = ['//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{0}]/td[1]/a/text()|//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{0}]/td[2]/text()'.format(i) for i in np.arange(1, 26)]
        path = '|'.join(path)
        result = html.xpath(path)
        return ({"ticker":result[i], "company_name":result[i+1]} for i in np.arange(0, 50, 2))

    def write_to_json(self, result):
        """Save the contents to a json file."""
        with open (self.filename,"a") as f:
            f.write(json.dumps(result) + '\n')

    def main(self):
        html = self.get_one_page()
        result = self.parse_one_page(html)
        for i in result:
            self.write_to_json(i)

if __name__=='__main__':
    offset = 25 # every page shows 25 tickers
    url = "https://finance.yahoo.com/screener/predefined/ms_energy/?count=25&offset={}"
    scraper = StockTickerScraper(offset, url)
    for i in np.arange(0, 8):
        scraper.url = url.format(i * scraper.offset)
        scraper.main()
        time.sleep(1)

