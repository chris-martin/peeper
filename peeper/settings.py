# Scrapy settings for peeper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
BOT_NAME = 'peeper'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['peeper.spiders']
NEWSPIDER_MODULE = 'peeper.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
  'peeper.pipelines.face_pipeline.FaceDetectPipeline',
  'peeper.pipelines.face_pipeline.FaceDownloadPipeline',
  'peeper.pipelines.face_pipeline.FaceProcessPipeline',
  'peeper.pipelines.json_pipeline.JsonWritePipeline',
]

