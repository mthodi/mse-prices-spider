## Malawi Stock Exchange Prices Spider
---
#### Description 
A web spider to get latest published stock prices from Malawi Stock Exchange and update [miyanda.org](https://www.miyanda.org). 

#### To run 
Install [scrapy]() and pdfttotext from [Poppler Utils](https://poppler.freedesktop.org/). Poppler utils are already installed on Ubuntu Linux. Make sure pdtotext is accessible from the Command Line / Terminal.

After scrapy and pdftotext are installed run

`$ python3 app.py`

The output is a SQL file to insert the data into a database. Feel free to modify as necessary e.g if one wanted to get an OHLC CSV file.
The database used by [miyanda.org](https://www.miyanda.org) is not included here, but if need arise one can infer the structure of 
the OHLC table from the SQL file produced.