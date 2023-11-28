# BestBuy-Product-Scraper

A Python-based web scraping tool that extracts product information from Best Buy's website. It allows users to search for products, check availability, and even simulate adding items to the shopping cart.

## Features
- Search products on Best Buy's website.
- Extract product details such as name, price, model, SKU number, and availability.
- Check inventory for specific products.
- Simulate adding items to the shopping cart.

## Installation

To use this scraper, you need to install the required Python packages:

```bash
pip install selenium beautifulsoup4 pandas requests
```
## Usage Example
```
from scraper import pageScraper

# Initialize with a URL
scraper = pageScraper('https://www.bestbuy.com/site/searchpage.jsp?st=product_name')

# Initialize with a product name
scraper.set_product_URL("product_name")
scraper.get_page()
```
