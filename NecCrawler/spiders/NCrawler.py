import scrapy
from scrapy import requests
from scrapy.conf import settings
from scrapy import Selector
from NecCrawler.items import NCArtistItem, NCAlbumItem, NCSongItem, NCLyricsItem

class NecSpider(scrapy.Spider):
    name = 'NecSpider'
    allowed_domain = ['http://music.163.com']
    start_urls = 'http://music.163.com/discover/artist/cat?id={gid}&initial={ini}'
    group_ids = [2001, 2002, 2003]
    headers = settings['DEFAULT_REQUEST_HEADERS']
    #referer = 'http://music.163.com'

    def start_request(self):
        for gid in self.group_ids:
            for i in range(65, 91):
                yield scrapy.Request(url=self.start_urls.format(gid=gid, ini=i), headers=self.headers,
                                                                method='GET', callback=self.parse)

    def parse(self, response):
        lists = response.selector.xpath('//*[@id="m-artist-box"]/li')
        for info in lists:
            item = NCArtistItem()
            try:
                item['artist_name'] = info.xpath('p/a[1]/text()').extract()[0]
                item['artist_id'] = info.xpath('p/a[1]/@href').extract()[0].split('=')[1]
                item['artist_album_url'] = 'http://music.163.com/artist/album?id=' + item['artist_id'] + '&limit=12&offset=0'
            except Exception:
                print('Error...')
            yield scrapy.Request(url=item['artist_album_url'], headers=self.headers, method='GET', callback=self.artist_parse)

    def artist_parse(self, response):
        lists = response.selector.xpath('//ul[@id="m-song-module"]/li')
        for info in lists:
            item = NCAlbumItem()
            try:
                item['album_name'] = info.xpath('div/@title').extract()[0]
                item['album_id'] = info.xpath('div/a[1]/@href').extract()[0].split('=')[1]
                item['release_date'] = info.xpath('p/span/text()').extract()[0]
                item['album_url'] = 'http://music.163.com/album?id=' + item['album_id']
            except Exception:
                print('Error...')
            yield scrapy.Request(url=item['album_url'], headers=self.headers, method='GET', callback=self.album_parse)

    def album_parse(self, response):
        lists = response.selector.xpath('//table[@class="m-table"]/tbody/tr')
        for info in lists:
            item = NCSongItem()
            try:
                sn = info.xpath('//span[@class="txt"]/a/b/@title').extract()[0].split('&nbsp;')
                name = ""
                for i in sn:
                    name = name + i + ' '
                item['song_name'] = name
                item['song_id'] = info.xpath('//span[@class="txt"]/a/@href').extract()[0].split('=').extract()[1]
                item['length'] = info.xpath('//span[@class="u-dur"]/text()').extract()[0]
                item['artist_name'] = info.xpath('td[4]/div/@title').extract()[0]
                item['song_url'] = 'http://music.163.com/song?id=' + item['song_id']
            except Exception:
                print('Error...')
            yield scrapy.Request(url=item['song_url'], headers=self.headers, method='GET', callback=self.song_parse)

    def song_parse(self, response):
        tit = response.selector.xpath('//div[@class="tit"]/em/text()').extract()[0]
        art = response.selector.xpath('//div[@class="cnt"]/p[1]/span/@title').extract()[0]
        lyr = response.selector.xpath('//div[@id="lyric-content"]')[0]
        lyr = lyr.xpath('string(.)')
        item = NCLyricsItem()
        item['title'] = tit
        item['artist'] = art
        item['lyrics'] = lyr
        yield item