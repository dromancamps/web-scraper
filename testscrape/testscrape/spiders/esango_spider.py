import re
import scrapy
from scrapy.link import Link

class EsangoSpider(scrapy.Spider):
    name = "esango"
    start_urls = ['https://esango.un.org/civilsociety/withOutLogin.do?method=getOrgsByTypesCode&orgTypeCode=6&orgTypName=Non-governmental%20organization&sessionCheck=false&ngoFlag=']

    def trimOrNull(self, value):
        return value if value is None else value.strip()

    def getValue(self, response, xpath):
        return response.xpath(xpath).get()

    def getValueAndTrim(self, response, xpath):
        return self.trimOrNull(self.getValue(response, xpath))

    def getValuesAndTrim(self, response, xpath):
        langs = response.xpath(xpath);
        arr = []
        if langs is not None:
            for lang in langs:
                arr.append(self.trimOrNull(lang.get()))
        return arr

    def getActivities(self, response):
        return []

    # Retrieves all necessary NGO data fields
    def parse_desc(self, response):
        yield {
#            'url': response.url,
            'title': self.getValueAndTrim(response, "/html/body/form/h3[1]/text()"),
            'acronym': self.getValueAndTrim(response, "/html/body/form/table[1]/tr[td[contains(text(), 'acronym')]]/td[2]/text()"),
            'phone': self.getValueAndTrim(response, "/html/body/form/table[1]/tr[td[contains(text(), 'Phone')]]/td[2]/text()"),
            'mail': self.getValueAndTrim(response, "/html/body/form/table[1]/tr[td[contains(text(), 'Email')]]/td[2]/text()"),
            'website': self.getValueAndTrim(response, "/html/body/form/table[1]/tr[td[contains(text(), 'Web site')]]/td[2]/text()"),
            'type': self.getValueAndTrim(response, "/html/body/form/table[1]/tr[td[contains(text(), 'Organization type')]]/td[2]/text()"),
            'languages': self.getValuesAndTrim(response, "/html/body/form/table[1]/tr[td[contains(text(), 'Languages')]]/td[2]/ul/li/text()"),
            'activities': self.getActivities(response),
            'scope': self.getValueAndTrim(response, "/html/body/form/table[3]/tr[td[contains(text(), 'scope')]]/td[2]/text()"),
            'country': self.getValuesAndTrim(response, "/html/body/form/table[3]/tr[td[contains(text(), 'Country')]]/td[2]/text()"),
            'statement': self.getValueAndTrim(response, ""),
            'funding': self.getValuesAndTrim(response, ""),
        }

    # Navigates through website and retrieves all NGO URLs
    def parse(self, response):

        for ngo in response.xpath("//*[@id='pagedResults1']/form/table/tr[@class='searchResult' or @class='searchResult differentColumn']/td[position()=3]"):
            
            url1 = ngo.xpath("img/@onclick").get();
            url_def = re.search("'(.*?)'", url1).group(1);
            
            yield response.follow(Link(url_def), self.parse_desc)

        next_page = response.xpath("//*[@id='paging']/a[position() = 3]")
        
        yield from response.follow_all(next_page, self.parse)