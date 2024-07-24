import scrapy
# from scraper.items import TheodoTeamItem
# import scrapy

class HackerNewsSpider(scrapy.Spider):
    name = "hacker_news"
    start_urls = [
        "https://news.ycombinator.com/"
    ]
    def parse(self, response):
        for article in response.css("tr.athing"):
            yield {
                "title": article.css("a.storylink::text").get(),
                "url": article.css("a.storylink::attr(href)").get(),
                "votes": int(article.css("span.score::text").re_first(r"\d+"))
            }
        next_page = response.css("a.morelink::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)



# class TheodoSpider(scrapy.Spider):
#     name = "theodo"
#     start_urls = ["https://www.theodo.co.uk/team"]

#     # this is what start_urls does
#     # def start_requests(self):
#     #     urls = ['https://www.theodo.co.uk/team',]
#     #     for url in urls:
#     #       yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         data = response.css("div.st-about-employee-pop-up")

#         for line in data:
#             item = TheodoTeamItem()
#             item["name"] = line.css("div.h3 h3::text").extract_first()
#             item["image"] = line.css("img.img-team-popup::attr(src)").extract_first()
#             item["fun_fact"] = line.css("div.p-small p::text").extract().pop()
#             yield item



# class QuotesSpider(scrapy.Spider):
#     name = 'quotes'
#     start_urls = ['http://quotes.toscrape.com/page/1/']
#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 'text': quote.css('span.text::text').get(),
#                 'author': quote.css('span small::text').get(),
#                 'tags': quote.css('div.tags a.tag::text').getall(),
#             }
#         next_page = response.css('li.next a::attr(href)').get()
#         if next_page is not None:
#             yield response.follow(next_page, self.parse)