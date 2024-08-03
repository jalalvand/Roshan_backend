from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.serializers import serialize
import re
from .models import Article
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
from rest_framework import viewsets
from .serializers import NewArticleSerializer
# from django_filters.rest_framework import DjangoFilterBackend
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# https://api2.zoomit.ir/editorial/api/articles/browse?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber=3

def extract_data(soup):
    

    atags = soup.find_all("a",class_=lambda value: value and ("BrowseArticleListItemDesktop" in value))
    print(atags)
    for atag in atags:
        itsurl = atag.get('href')
        # print(itsurl)
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
                print(article)
                article.save()
        
        except :
            pass
    


def scrape_website(url):
    # async with AsyncHTMLSession() as session:
    #     r = await session.get(url)
    #     await r.html.arender(sleep=30)
    #     data = r.html.full_text
    #     print(data)
    
    # driver = webdriver.Chrome()
    # driver.get(url)
    # element = WebDriverWait(driver,100).until(EC.url_contains(url))
    
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # page_source = driver.page_source
    # soup = BeautifulSoup(page_source, "html.parser")
    
    session = HTMLSession()
    r = session.get(url, verify=False)
    print(r.status_code)
    r.html.arender(sleep=30)
    text = r.html.raw_html
    soup = BeautifulSoup(text,"html.parser")
    # print(soup)    
    extract_data(soup)
    session.close()

    # numofpages = int(500/50)
    
    # for i in range(2,numofpages):
    #     r = session.get(url+f"{i}")
    #     print(r.status_code)
    #     if(r.status_code == 200):
    #         print("in if ")
    #         r.html.arender(sleep=30)
    #         text = r.html.html
    #         soup = BeautifulSoup(text,"html.parser")
    #         print(soup)
    #         extract_data(soup)

def first_scrapy(url):
    session = HTMLSession()
    # numofpages = int(500/50)
    try:
        r = session.get(url)
    except:
        pass
    print(r.status_code)
    if(r.status_code == 200):
        print("************")
        r.html.arender(sleep=30)
        text = r.html.html
        
        soup = BeautifulSoup(text,"html.parser")
        extract_data(soup)
    # for i in range(2,numofpages):
    #     try:
    #         r = session.get(url+f"{i}")
    #     except:
    #         continue
    #     print(r.status_code)
    #     if(r.status_code == 200):
    #         print("************")
    #         r.html.arender(sleep=30)
    #         text = r.html.html
    #         soup = BeautifulSoup(text,"html.parser")
    #         extract_data(soup)

def peridic_scrapy(url):
    session = HTMLSession()
    numofpages = int(500/50)
    r = session.get(url)
    print(r.status_code)
    if(r.status_code == 200):
        r.html.arender(sleep=30)
        text = r.html.html
        soup = BeautifulSoup(text,"html.parser")
        extract_data(soup)
        

    
class NewArticleViewSet(viewsets.ModelViewSet):
    # url = 'https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber='
    # first_scrapy(url)
    queryset = Article.objects.all()
    serializer_class = NewArticleSerializer




def scrape_view(request):
    # url = 'https://www.zoomit.ir/'
    url = 'https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber='
    data = scrape_website(url)
    # return JsonResponse({Article.objects.all()})
    qs = Article.objects.all()
    data = serialize("json", qs)
    return HttpResponse(data, content_type="application/json")
    
