from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
import re
from .models import Article
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



def scrape_website(url):
    data = []
    response = requests.get(url)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Example: Extracting all headings
    articlass = re.compile("Article")
    # headings = soup.find_all('div',class_=articlass)
    divs = soup.find_all("div", class_=lambda value: value and value.startswith("Article"))
    for div in divs:
        a_tags = div.find_all('a')
        for a in a_tags:
            # print(a.get('href'), a.text)
            itsurl = a.get('href')
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
                # print(headercontent)
                headerdivs = headercontent.find_all("div") 
                # print(len(headerdivs))
        #         # firstdiv = headerdivs[0]
                
                for d in headerdivs:
                    atage_d = d.find_all("a")
                    partdata = []
                    for aaa in atage_d:
                        # print(aaa.text)
                        partdata.append(aaa.text)
                    
                    alldata.append(partdata)
            try:
                # print(alldata[0])
                if(len(alldata) != 0 and len(alldata[0]) != 0):
                    # print(alldata[0])
                    source = alldata[0][len(alldata[0])-1]
                    tagslist = alldata[0][:len(alldata[0])-1]
                    tagstring = ','.join(map(str, tagslist))
                    article = Article(
                    title=title,
                    content=content,
                    url=itsurl,
                    tag = tagstring,
                    resource=source
                    )   
                    print(article)
                    article.save()
            
            except :
                pass 
            
            

            # if(len(alldata) > 0):
            #     print(alldata[0])
    # for row in headings: 
    #     print(row)
        # print( row.a['href']) 
    # print(headings)
    # return headings
    return "Hello"
# [h.text for h in divs]


def scrape_view(request):
    url = 'https://www.zoomit.ir/'
    data = scrape_website(url)
    return JsonResponse({'headings': data})
    # return data