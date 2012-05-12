# the models for scraped items

from scrapy.item import Item, Field

class PeeperItem(Item):
    img_url = Field()
    name = Field()
