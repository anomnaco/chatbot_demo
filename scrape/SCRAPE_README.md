## Scraper Readme

# Setup

This scraper uses Selenium and a headless chrome browser to load interactive elements of web pages.

To install Google Chrome run:

```
sudo apt-get install google-chrome
```

Also install the chrome driver:

```
sudo apt install chromium-chromedriver
```

Then clone this repo and install the Python requirements (This demo assumes you already have python3 installed):
```
git clone https://github.com/Anant/astra-chatbot-react-python.git
cd astra-chatbot-react-python/scrape
pip3 install -r requirements.txt
```

You can add and remove urls to scrape by modifying the list urls on line 19 inside the astra_scraper.py file. You can also change the name of the output file on line 76 of the same file. The file scraped_results.json contains the results from ruunning the astra_scraper.py scccript with the default values for urls and output filename.

# Start Process

To run the scraper enter the command:
```
python3 astra_scraper.py
```
