# item pipelines

import json

class PeeperPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item)) + "\n")
        return item

