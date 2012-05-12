from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from peeper.items import PeeperItem

class GtIsyeSpider(CrawlSpider):
    name = 'gt-isye'
    allowed_domains = ['www.isye.gatech.edu']
    start_urls = ['http://www.isye.gatech.edu/people/alpha-listing.php']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'http://www.isye.gatech.edu/faculty-staff/profile.php?'),
            callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = PeeperItem()
        i['img_url'] = next(iter(hxs.select('//div[@id="content_sub"]//img/@src').extract()), None)
        i['name'] = next(iter(hxs.select('//div[@id="content_sub"]//h2/text()').extract()), None)
        return i
