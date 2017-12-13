# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NeccrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NCArtistItem(scrapy.Item):

    _id = scrapy.Field()
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()
    artist__album_url = scrapy.Field()
    #album_urls = scrapy.Field()

class NCAlbumItem(scrapy.Item):

    _id = scrapy.Field()
    album_name = scrapy.Field()
    album_id = scrapy.Field()
    release_date = scrapy.Field()
    album_url = scrapy.Field()
    #track_num = scrapy.Field()
    #artist_name = scrapy.Field()
    #release_date = scrapy.Field()
    #comment_num = scrapy.Field()

class NCSongItem(scrapy.Item):

    _id = scrapy.Field()
    song_name = scrapy.Field()
    song_id = scrapy.Field()
    length = scrapy.Field()
    artist_name = scrapy.Field()
    song_url = scrapy.Field()
    #comment_num = scrapy.Field()
    #lyrics = scrapy.Field()

class NCLyricsItem(scrapy.Item):

    _id = scrapy.Field()
    title = scrapy.Field()
    artist = scrapy.Field()
    lyrics = scrapy.Field()
