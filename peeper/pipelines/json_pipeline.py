import json
import os

class JsonWritePipeline(object):

    def __init__(self):
        if not os.access('output', os.F_OK): os.makedirs('output')
        self.file = open('output/items.jl', 'wb')

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item)) + "\n")
        return item
