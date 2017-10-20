from bs4 import BeautifulSoup
import csv
import re
import requests
import sys

def scrape_data(ticker):
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={ticker}"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    company_tag = soup.find('span', attrs={'class': 'companyName'})
    company_name = company_tag.text.split("CIK")[0].strip()
    ident_tag = soup.find('p', attrs={'class':'identInfo'})
    sic = ident_tag.find('a').text
    sector = re.findall(r'SIC:\s*\d+?\s*-\s*(.+?)State', ident_tag.text)[0]
    return [ticker, company_name, sic, sector]

if __name__=='__main__':
    tickers_file = sys.argv[1]
    csv_file = sys.argv[2]
    with open(tickers_file) as fin, open(csv_file, 'wt') as fout:
        csvout = csv.writer(fout)
        csvout.writerow(['Ticker','Name','SIC','Sector', 'Addr1'])
        for line in fin:
            ticker = line.strip()
            data = scrape_data(ticker)
            csvout.writerow(data)
