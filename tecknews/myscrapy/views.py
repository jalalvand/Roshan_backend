import urllib.request
import json
from rest_framework import viewsets
from .serializers import NewArticleSerializer
from .models import Article
from django.core.serializers import serialize
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

def extract_data(itsurl):
    
    if (Article.objects.filter(url=itsurl).first() != None):
        return
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
        if(headercontent != None ):
            atage_d = headercontent.find_all("a")
            partdata = []
            for aaa in atage_d:
                partdata.append(aaa.text)
            # print(partdata)    
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



def peridic_scrapy():
    prepare_to_extractdata(1)



class NewArticleViewSet(viewsets.ModelViewSet):
    # url = 'https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber='
    # first_scrapy(url)
    queryset = Article.objects.all()
    serializer_class = NewArticleSerializer
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [SearchFilter]
    search_fields = ['@tag']
    # filterset_fields = ['tag']
    



def scrape_view(request):
    # url = 'https://www.zoomit.ir/'
    # url = 'https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber='
    # data = scrape_website(url)
    # return JsonResponse({Article.objects.all()})
    qs = Article.objects.all()
    data = serialize("json", qs)
    return HttpResponse(data, content_type="application/json")

def geeting_data_zoomit():
    numofpages = 100
    """ برای اینکه گرفتن اطلاعات از این صفحات خیلی طول نشکه 4 صفحه اول در نظر میگیریم."""
    for i in range(1,4):
        print(i)
        prepare_to_extractdata(i)
        

def prepare_to_extractdata(pag_num):
    url = f"https://api2.zoomit.ir/editorial/api/articles/browse?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber={pag_num}"

    with urllib.request.urlopen(url) as response:
        body_json = response.read()

    body_dict = json.loads(body_json)
    jsons = body_dict["source"]
    for x in jsons:
        baseurl = "https://www.zoomit.ir/"
        slug = ""
        has_notslug = False
        try:
            slug = x["slug"]
        except:
            has_notslug = True
            # print(x)
            # print(e)
        title = x["title"]
        resource = x["author"]["fullName"]
        itsurl = baseurl + slug
        if(has_notslug):
            itsurl = x["link"]
        extract_data(itsurl)
        print(f"extracting data of {itsurl} done.")
    



def main():
    geeting_data_zoomit()
    # print(body_dict)

# if __name__ == "__main__":
#     print("in main")
    
main()