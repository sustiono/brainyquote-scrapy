# Brainyquote Scrapy

Scrap quotes from https://www.brainyquote.com/topics using Scrapy

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install some packages needed.

```bash
git clone git@github.com:sustiono/brainyquote-scrapy.git
cd brainyquote-scrapy
pip3 install virtualenv
virtualenv .env
source .env/bin/activate
cd brainyquote
pip install -r requirements.txt
```

## Usage
Choose one of the commands below to get the results in the desired format

```bash
scrapy crawl quotes -o quotes.csv
scrapy crawl quotes -o quotes.json
scrapy crawl quotes -o quotes.xml
```
