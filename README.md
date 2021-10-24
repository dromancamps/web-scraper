## How project has been created

1. Create virtual environment: `python3 -m venv venv`.
2. Activate environment: `source venv/bin/activate`.
3. Install scrapy: `pip3 install scrapy`.
4. Create scrapy project: `scrapy startproject testscrape`.
5. Create spider in testscreape/spiders folder.

## Usage

Go to testscreape direcotry (outer one), and execute `scrapy crawl post -O test.json`.
This will save the result in test.json file

## Advice

Remember to remove (or not to add) `tbody` in XPath.