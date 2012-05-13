# the models for scraped items

from scrapy.item import Item, Field

class PeeperItem(Item):
    url = Field()
    name = Field()
    img_urls = Field()
    face_url = Field()
    face_info = Field()
    face_file = Field()
