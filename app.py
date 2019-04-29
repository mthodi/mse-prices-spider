#!/usr/bin/python3

from scrapy.crawler import CrawlerProcess
from mse_prices import MsePricesSpider
import os, sys

process = CrawlerProcess({
    'USER AGENT' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(MsePricesSpider)
process.start()

# TODO: get the close status of the spider...if closed then quit
with open('status.txt', 'r') as file:
    status = file.readline().splitlines()[0]
if status == 'CLOSED':
    sys.exit(-1)

# convert data to PDF
os.system('./pdf_to_sql.sh {}'.format(status))
# load data into database
sql_file = status.split('.')[0] + '.sql'
os.system('./insert_into_db.sh {}'.format(sql_file))
