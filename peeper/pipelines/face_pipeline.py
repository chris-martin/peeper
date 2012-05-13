from face_client import FaceClient
import os
from urllib2 import urlopen
import hashlib
from PIL import Image

import peeperconfig

fc = FaceClient(
    api_key = peeperconfig.FACE_API_KEY, 
    api_secret = peeperconfig.FACE_API_SECRET,
)

class FaceDetectPipeline(object):

    def process_item(self, item, spider):
        if item.has_key('img_urls'):
            self.process_images(item)
        return item

    def process_images(self, item):
        for url in item['img_urls']:
            d = self.face_detect(url)
            if d:
                item['face_url'] = url
                item['face_info'] = d
                return

    def face_detect(self, url):
        result = fc.faces_detect(urls = url)
        tags = result['photos'][0]['tags']
        if len(tags) is not 1: return
        tag = tags[0]
        return tag

class FaceDownloadPipeline(object):

    def process_item(self, item, spider):
        if all(k in item for k in ('face_url', 'face_info')):
            url = item['face_url']
            filename = hashlib.sha1(url).hexdigest()
            item['face_file'] = filename
            remote = urlopen(url)
            if not os.access('output/face/raw', os.F_OK): os.makedirs('output/face/raw')
            local = open('output/face/raw/%s' % filename, 'wb')
            local.write(remote.read())
            local.close()
        return item

class FaceProcessPipeline(object):

    def process_item(self, item, spider):
        if all(k in item for k in ('face_info', 'face_file')):
            im = Image.open('output/face/raw/%s' % item['face_file'])
            info = item['face_info']
            bbox = im.getbbox()
            bwidth = bbox[2] - bbox[0]
            bheight = bbox[3] - bbox[1]
            cbox = (
              max(bbox[0], int(bwidth * (info['center']['x'] - info['width']  / 2)) / 100),
              max(bbox[1], int(bheight * (info['center']['y'] - info['height'] / 2)) / 100),
              min(bbox[2], int(bwidth * (info['center']['x'] + info['width']  / 2)) / 100),
              min(bbox[3], int(bheight * (info['center']['y'] + info['height'] / 2)) / 100),
            )
            im = im.crop(cbox)
            if not os.access('output/face/processed', os.F_OK): os.makedirs('output/face/processed')
            im.save('output/face/processed/%s.jpg' % item['face_file']);
        return item
