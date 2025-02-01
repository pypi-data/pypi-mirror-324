# ProxyScraper

## Overview
ProxyScraper is a Python package designed to scrape free proxy lists from various online sources. It uses multithreading to enhance performance and efficiently gather proxies.

## Features
- Fetches free proxies from multiple sources
- Uses multithreading for better performance
- Automatically formats proxies into `IP:PORT`
- Simple and easy-to-use interface

## Installation
You can install ProxyScraper via GitHub or PyPI.

### Install from GitHub
```sh
pip install git+https://github.com/alfarttusie/proxyscraper.git
```

### Install from PyPI
```sh
pip install online-proxy-scraper
```

## Usage
```python
from proxyscraper import ProxyScraper

scraper = ProxyScraper()
print(scraper.list)  # List of formatted proxies
```

## Dependencies
- `requests`

## License
MIT License

## Author
[alfarttusie](https://github.com/alfarttusie)

