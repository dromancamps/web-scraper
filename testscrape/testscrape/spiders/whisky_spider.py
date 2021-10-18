import scrapy

class PostSpider(scrapy.Spider):
    name = "whisky"
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def parse(self, response):

        # with open('whisky.html', 'wb') as f:
        #     f.write(response.body)
        
        for products in response.css('div.product-item-info'):
            yield {
                'name': products.css('a.product-item-link::text').get(),
                'price': products.css('span.price::text').get().replace('£', ''),
                'link': products.css('a.product-item-link').attrib['href']
            }
