import re
import scrapy
from scrapy.link import Link

class EsangoSpider(scrapy.Spider):
    name = "esango"
    start_urls = ['https://esango.un.org/civilsociety/withOutLogin.do?method=getOrgsByTypesCode&orgTypeCode=6&orgTypName=Non-governmental%20organization&sessionCheck=false&ngoFlag=']

    def parse_desc(self, response):
        yield {
            'title': response.xpath("/html/body/form/h3[1]/text()").get()
        }

    def parse(self, response):

        for ngo in response.xpath("//*[@id='pagedResults1']/form/table/tr[@class='searchResult' or @class='searchResult differentColumn']/td[position()=3]"):
            
            # window.open('./showProfileDetail.do?method=printProfile&tab=1&profileCode=2940');
            url1 = ngo.xpath("img/@onclick").get();
            url_def = re.search("'(.*?)'", url1).group(1);
            
            yield response.follow(Link(url_def), self.parse_desc)

        next_page = response.xpath("//*[@id='paging']/a[position() = 3]")
        
        yield from response.follow_all(next_page, self.parse)