# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import codecs
#from twisted.enterprise import adbapi
#from logging import log
#import json
from scrapy.conf import settings
from NecCrawler.items import NCArtistItem,NCAlbumItem,NCSongItem,NCLyricsItem

class NeccrawlerPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        self.client = pymongo.MongoClient(host=host, port=port)
        self.tdb = self.client[db_name]
        self.post = self.tdb[settings['MONGODB_DOCNAME_ARTIST']]


    def process_item(self, item, spider):
        if isinstance(item, NCArtistItem):
            try:
                artist_info = dict(item)
                if self.post.insert(artist_info):
                    print('Artist successful!')
            except Exception:
                pass
        if isinstance(item, NCAlbumItem):
            try:
                album_info = dict(item)
                if self.post.insert(album_info):
                    print('Album successful!')
            except Exception:
                pass
        if isinstance(item, NCSongItem):
            try:
                song_info = dict(item)
                if self.post.insert(song_info):
                    print('Song successful!')
            except Exception:
                pass
        if isinstance(item, NCLyricsItem):
            try:
                lyrics_info = dict(item)
                if self.post.insert(lyrics_info):
                    print('Lyrics successful!')
            except Exception:
                pass

    def _handle_error(self, failure, item, spider):
        print (failure)

#class JsonWithEncodingPipeline(object):
#
#    def __init__(self):
#        self.file = codecs.open('info.json', 'w', encoding='utf-8')
#
#    def process_item(self):
#        line = json.dumps(dict(item)) + '\n'
#        self.file.write(line)
#        return item
#
#    def spider_closed(self, spider):
#        self.file.close()

