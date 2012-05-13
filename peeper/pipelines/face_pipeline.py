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
            bound = self.bound(im)
            face = self.face(bound, info)
            size = self.size(bound, face)

            # push the box up a little
            face['center']['y'] -= size * 0.2

            o = {
                'x': min(bound['x'][1] - size, max(bound['x'][0], face['center']['x'] - size / 2)),
                'y': min(bound['y'][1] - size, max(bound['y'][0], face['center']['y'] - size / 2)),
            }

            im = im.crop((
                int(o['x']),
                int(o['y']),
                int(o['x'] + size),
                int(o['y'] + size)
            ))
            if not os.access('output/face/processed', os.F_OK): os.makedirs('output/face/processed')
            im.save('output/face/processed/%s.jpg' % item['face_file']);
        return item

    # the width/height of the square cropped box
    def size(self, bound, face):
        return min(
            bound['size']['x'],
            bound['size']['y'],
            2.5 * max(
                face['size']['x'],
                face['size']['y'],
            ),
        )

    # convert percentages to pixels
    def face(self, bound, info):
        return {
            'center': {
                'x': bound['size']['x'] * info['center']['x'] / 100,
                'y': bound['size']['y'] * info['center']['y'] / 100,
            },
            'size': {
                'x': bound['size']['x'] * info['width'] / 100,
                'y': bound['size']['y'] * info['height'] / 100,
            },
        }

    # just reformat the result of im.getbbox()
    def bound(self, im):
        bbox = im.getbbox()
        return {
            'size': {
                'x': bbox[2] - bbox[0],
                'y': bbox[3] - bbox[1],
            },
            'x': [
                bbox[0],
                bbox[2],
            ],
            'y': [
                bbox[1],
                bbox[3]
            ],
        }
