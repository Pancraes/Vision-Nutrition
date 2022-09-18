import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup
import requests


class Scraper:
    links = []
    names = []

    def __init__(self, query_dict):
        self.query_dict = query_dict

    def get_url(self, url):
        url = requests.get(url).text
        self.soup = BeautifulSoup(url, 'lxml')

    def print_info(self):
        base_url = "https://allrecipes.com/search/results/?"
        query_url = urllib.parse.urlencode(self.query_dict, doseq=True)
        url = base_url + query_url
        self.get_url(url)
        name = self.query_dict['search']

        # Count the number of search results
        resp = str(self.soup.find(
            'span', class_="search-results-total-results")).strip(' ')
        resp = ''.join(re.findall('\d+', resp))

        # Check if the search returns no results
        if resp == '0':
            print(f'No recipes found for {name}')
            return
        
        ret=[]
        articles = self.soup.find_all("div", class_= "card__recipe")
        info = self.soup.find_all('div', class_="card__detailsContainer")
        for i in range(max(len(articles), 4)):
            data={}
            
            name=articles[i].find("a", title=re.compile(''))['title']
            data['name']=name

            img=articles[i].find("a", href=re.compile('^https://www.allrecipes.com/recipe/')).find("img")["src"]
            data['image']=img

            url = articles[i].find("a", href=re.compile('^https://www.allrecipes.com/recipe/'))['href']
            data["url"]=url

            #detailed info
            self.get_url(data["url"])

            ingredient_spans = self.soup.find_all('span', class_='ingredients-item-name')
            ingredients = [span.text.strip() for span in ingredient_spans]
            data['ingredients']=ingredients

            if data and 'image' in data:
                ret.append(data)
        
        print(ret)
        return ret


def allrecipes(recipeName, ingIncl, ingExcl):
    query_dict = {
        "search": recipeName,     # Query keywords
        # 'Must be included' ingrdients (optional)
        "ingIncl": ingIncl,
        # 'Must not be included' ingredients (optional)
        "ingExcl": ingExcl,
        # Sorting options : 're' for relevance,\
        #  'ra' for rating, 'p' for popular (optional)
        "sort": "re"
    }
    scrap = Scraper(query_dict)
    scrap.print_info()


allrecipes('',['tomato', 'potato', 'onion', 'cucumber'],['chicken', 'beef', 'lamb'])