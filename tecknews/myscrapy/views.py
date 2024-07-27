from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.serializers import serialize
import re
from .models import Article
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from requests_html import HTMLSession


def extract_data(soup):
    atags = soup.find_all("a",class_=lambda value: value and ("BrowseArticleListItemDesktop" in value))
    for atag in atags:
        itsurl = atag.get('href')
        if (Article.objects.filter(url=itsurl).first() != None):
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
    


def scrape_website(url):
    session = HTMLSession()
    r = session.get(url)
    print(r.status_code)
    r.html.arender(sleep=30)
    text = r.html.html
    soup = BeautifulSoup(text,"html.parser")
    # pages = soup.find_all("div",class_=lambda value: value and ("PaginationContainer" in value))
    # pages = soup.find_all("div",class_=lambda value: value and ("Pagination" in value))
    # print(pages)
    # for page in pages:
    #     butts = page.find_all("button")
    #     for but in butts:
    #         print(but.text)
    
    extract_data(soup)

    numofpages = int(500/50)
    
    for i in range(2,numofpages):
        r = session.get(url+f"{i}")
        print(r.status_code)
        if(r.status_code == 200):
            r.html.arender(sleep=30)
            text = r.html.html
            soup = BeautifulSoup(text,"html.parser")
            extract_data(soup)
        
    
     
    

def scrape_view(request):
    # url = 'https://www.zoomit.ir/'
    url = 'https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber='
    data = scrape_website(url)
    # return JsonResponse({Article.objects.all()})
    qs = Article.objects.all()
    data = serialize("json", qs)
    return HttpResponse(data, content_type="application/json")
    




