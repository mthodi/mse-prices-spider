# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from datetime import datetime

class MsePricesSpider(scrapy.Spider):
    name = 'mse_prices'
    allowed_domains = ['mse.co.mw']
    start_urls = ['https://mse.co.mw/index.php?route=market/market/report']

    def parse(self, response):
        # TODO: verify that it is a daily report
        pdf_url =  response.css("a.btn::attr(href)").extract()[0]
        with open('latest.txt', 'r') as file: 
            recent_url = file.readline().splitlines()[0]
        if pdf_url == recent_url:
            with open('status.txt', 'w') as file:
                file.write('CLOSED')
            raise CloseSpider('No new reports to download')
        with open('latest.txt', 'w') as file:
            file.write(pdf_url)
        yield Request(
            url=pdf_url,
            callback=self.save_pdf
        )
    
    def save_pdf(self, response):
        """Saves the downloaded prices PDF"""
        output_file= datetime.today().strftime('daily_%d_%B_%Y.pdf')
        self.logger.info("[+] Saving report at {}".format(output_file))
        with open(output_file, 'wb') as file:
            file.write(response.body)
        with open('status.txt', 'w') as file:
            file.write(output_file)


