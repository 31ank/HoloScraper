# HoloScraper
https://schedule.hololive.tv/ scraper made with python

## Python dependencies
The scraper was created with Python 3.8.3
* Requests to generate http requests ```pip install requests```
* Beautifulsoup4 for parsing HTML ```pip install beautifulsoup4```
* MySQL connector to connect to db ```pip install mysql-connector-python```
* pytz to convert timezones ```pip install pytz```

## Setup
_Database template coming soon_<br>
Insert you database credentials in database-default.py and rename it to database.py.
Setup your database with the database template.
You can now run ```python scraper.py``` and it will automatically fill your database.