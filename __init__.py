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

        # Collect all the search results in a BS4 element tag
        articles = self.soup.find_all('div', class_="card__detailsContainer")

        texts = []
        for article in articles:
            txt = article.find('div', class_='card__detailsContainer-left')
            if txt:
                if len(texts) < 5:
                    texts.append(txt)
                else:
                    break
        self.links = [txt.a['href'] for txt in texts]
        self.names = [txt.h3.text for txt in texts]
        self.get_data()

    def get_data(self):
        self.ingredientsList = []
        self.instructionsList = []
        for i, link in enumerate(self.links):
            self.get_url(link)
            print('-' * 4 + self.names[i] + '-' * 4)
            info_names = [div.text.strip() for div in self.soup.find_all(
                'div', class_='recipe-meta-item-header')]
            ingredient_spans = self.soup.find_all(
                'span', class_='ingredients-item-name')
            instructions_spans = self.soup.find_all('div', class_='paragraph')
            ingredients = [span.text.strip() for span in ingredient_spans]
            instructions = [span.text.strip() for span in instructions_spans]
            for i, div in enumerate(self.soup.find_all('div',
                                                       class_='recipe-meta-item-body')):
                print(info_names[i].capitalize(), div.text.strip())
            print()
            print('Ingredients'.center(len(ingredients[0]), ' '))
            print('\n'.join(ingredients))
            print()
            print('Instructions'.center(len(instructions[0]), ' '))
            # print((count, instruction) for count,
            #       instruction in zip(range(len(instructions)), instructions))
            print('\n'.join(instructions))
            print()
            print('*' * 50)
            self.ingredientsList.append(ingredients)
            self.instructionsList.append(instructions)


def main():
    recipeName = "Chicken Stew"
    ingIncl = ""
    ingExcl = ""
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


if __name__ == '__main__':
    main()