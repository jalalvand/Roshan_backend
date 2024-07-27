from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.serializers import serialize
import re
from .models import Article
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_website(url):
    
    driver = webdriver.Chrome()
    driver.get(url)
    element = WebDriverWait(driver,100).until(EC.url_contains(url))
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    atags = soup.find_all("a",class_=lambda value: value and ("BrowseArticleListItemDesktop" in value))
    for atag in atags:
        itsurl = atag.get('href')
        if (Article.objects.filter(url=itsurl) != None):
            continue
        urlrespo = requests.get(itsurl)
        urlsoup = BeautifulSoup(urlrespo.text, 'html.parser')
        p_tags = urlsoup.find_all('p')

        # Concatenate the content of all <p> tags
        content = ' '.join(p.get_text() for p in p_tags)
        title = urlsoup.find("title").text
        # print(title)
        artcontent = urlsoup.find("article")
        alldata = []
        if(not artcontent == None):
            headercontent = artcontent.find("header",class_=lambda value: value and value.startswith("ArticleHeader"))
            
            atage_d = headercontent.find_all("a")
            partdata = []
            for aaa in atage_d:
                partdata.append(aaa.text)
            print(partdata)    
        try:
            if(len(partdata) != 0 ):
                source = partdata[len(partdata)-1]
                tagslist = partdata[:len(partdata)-1]
                tagstring = ','.join(map(str, tagslist))
                article = Article(
                title=title,
                content=content,
                url=itsurl,
                tag = tagstring,
                resource=source
                )   
                # print(article)
                article.save()
        
        except :
            pass 
        
    

def scrape_view(request):
    # url = 'https://www.zoomit.ir/'
    url = 'https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber=1'
    data = scrape_website(url)
    # return JsonResponse({Article.objects.all()})
    qs = Article.objects.all()
    data = serialize("json", qs)
    return HttpResponse(data, content_type="application/json")
    






# <div class="flex__Flex-le1v16-0 fJGOfb">


# def scrape_website(url):
#     # for i in range(1,3):
#     #     url = url + f"{i}"
#     #     print(url)
#     data = []
#     response = requests.get(url)
#     # print(response.text)
#     soup = BeautifulSoup(response.content, 'html5lib')
#     # Example: Extracting all headings
#     # body = soup.find_all('body')
#     # print(body)
    
#     # divs = soup.find_all("div", class_=lambda value: value and value.startswith("flex__Flex-le1v16-0 rJAYV"))
#     # divs = soup.find_all('div', {'style': lambda s: s and 'scroll-margin' in s})
#     # divs = soup.find_all("div", id=lambda value: value and  value == "__next")
#     divs = soup.find_all("a", class_=lambda value: value and "CustomNextLink" in value)
#     # divs = soup.find_all("div")
#     # divs = divs.find_all("div")
#     # print(divs)
#     for div in divs: 
#         print(div.get('href'))
#         # atags = div.find_all("a", class_=lambda value: value and "CustomNextLink" in value)
#         # for a in atags:
#         #     print(a.get('href')) 
#         # style = div.get('style')
#         # print(style)
#         # if(not "scroll-margin" in style):
#         #     continue
#         # a_tags = div.find_all('a')
#         # for a in a_tags:
#         #     # print(a.get('href'), a.text)
#         #     itsurl = a.get('href')
#         #     urlrespo = requests.get(itsurl)
#         #     urlsoup = BeautifulSoup(urlrespo.text, 'html.parser')
#         #     p_tags = urlsoup.find_all('p')
    
#         #     # Concatenate the content of all <p> tags
#         #     content = ' '.join(p.get_text() for p in p_tags)
#         #     title = urlsoup.find("title").text
#         #     print(title)
#         #     artcontent = urlsoup.find("article")
#         #     alldata = []
#         #     if(not artcontent == None):
#         #         headercontent = artcontent.find("header",class_=lambda value: value and value.startswith("ArticleHeader"))
                
#         #         atage_d = headercontent.find_all("a")
#         #         partdata = []
#         #         for aaa in atage_d:
#         #             # print(aaa.text)
#         #             partdata.append(aaa.text)
#         #         print(partdata)    
#         #     try:
#         #         # print(alldata[0])
#         #         if(len(partdata) != 0 ):
#         #             # print(alldata[0])
#         #             source = partdata[len(partdata)-1]
#         #             tagslist = partdata[:len(partdata)-1]
#         #             tagstring = ','.join(map(str, tagslist))
#         #             article = Article(
#         #             title=title,
#         #             content=content,
#         #             url=itsurl,
#         #             tag = tagstring,
#         #             resource=source
#         #             )   
#         #             # print(article)
#         #             article.save()
            
#         #     except :
#         #         pass 
            
            

#             # if(len(alldata) > 0):
#             #     print(alldata[0])
#     # for row in headings: 
#     #     print(row)
#         # print( row.a['href']) 
#     # print(headings)
#     # return headings
#     return "Hello"
# # [h.text for h in divs]




    

# from scrapy.crawler import CrawlerProcess
# from scraper.scraper.spiders.myspider import HackerNewsSpider

# def scrape_hacker_news(request):
#     process = CrawlerProcess(settings={
#         "FEEDS": {
#             "items.json": {"format": "json"},
#         },
#     })
#     process.crawl(HackerNewsSpider)
#     process.start()
#     with open("items.json", "r") as f:
#         data = f.read()
#     return JsonResponse(data, safe=False)
