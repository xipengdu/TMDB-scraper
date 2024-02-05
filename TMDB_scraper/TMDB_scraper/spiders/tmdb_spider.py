# to run 
# scrapy crawl tmdb_spider -o movies.csv -a subdir=671-harry-potter-and-the-philosopher-s-stone

import scrapy
from scrapy.selector import Selector
import requests


class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    user_agent = {"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    # utilizing user agent to crawl
    def __init__(self, subdir=None, *args, **kwargs):
        self.start_urls = [f"https://www.themoviedb.org/movie/{subdir}/"]


    def parse(self, response):
        current_url = response.urljoin(f'{response.url}/cast')  # problem is that spider wont go to "cast"
        yield scrapy.Request(current_url, callback=self.parse_full_credits) 

    def parse_full_credits(self, response):
        self.actors = {"actor": response.xpath("//div[@class='info']/p/a/text()").getall(), 
                         "web": response.xpath("//div[@class='info']/p/a/@href").getall()}
        for i in range(len(self.actors["actor"])):
            yield scrapy.Request("https://www.themoviedb.org" + self.actors["web"][i] + "?credit_department=Acting", callback=self.parse_actor_page)



    def parse_actor_page(self, response):
        actor_name = response.xpath("//h2[@class='title']/a/text()").get()
        movie_or_TV_name_list = response.xpath("//a[@class='tooltip']/bdi/text()").getall()
        for movie_or_TV_name in movie_or_TV_name_list:
            yield {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}

    #  scrapy crawl tmdb_spider -o results.csv -a subdir=671-harry-potter-and-the-philosopher-s-stone