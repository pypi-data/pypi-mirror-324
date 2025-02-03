# pcdt-scraper

A PyChromeDevTools based WebScraper and selenium like syntax.

[![Python package](https://github.com/jakbin/pcdt-scraper/actions/workflows/publish.yml/badge.svg)](https://github.com/jakbin/pcdt-scraper/actions/workflows/publish.yml)
[![PyPI version](https://badge.fury.io/py/pcdt-scraper.svg)](https://pypi.org/project/pcdt-scraper)
[![Downloads](https://pepy.tech/badge/pcdt-scraper/month)](https://pepy.tech/project/pcdt-scraper)
[![Downloads](https://static.pepy.tech/personalized-badge/pcdt-scraper?period=total&units=international_system&left_color=green&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/pcdt-scraper)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jakbin/pcdt-scraper)
![GitHub last commit](https://img.shields.io/github/last-commit/jakbin/pcdt-scraper)

## Introduction

Sometimes website blocks your requests or aiohttp web request but don't block chrome web request.  

For this solution, here is "pcdt-scraper".

## Compatability

Python 3.6+ is required.

## Installation

```sh
pip install pcdt-scraper
```

or 

```sh
pip3 install pcdt-scraper
```

## Usage:

1. First run chromium or chrome remote instance

```sh
chromium --remote-debugging-port=9222 --remote-allow-origins=*

```
or You can run as headless mode.

```sh
chromium --remote-debugging-port=9222 --remote-allow-origins=* --headless
```

2. Then run python code

```py
from pcdt_scraper import WebScraper

scraper = WebScraper()
url = "https://www.example.com/"
try:
    # Navigate to a page
    if scraper.get(url):

        # Get page content
        content = scraper.get_page_content()

        # find element by class name
        text = scraper.find_element_by_class_name('class_name').text()
        print(text)

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    scraper.close()
```
