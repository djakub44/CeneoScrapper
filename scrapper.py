

import requests as re
from bs4 import BeautifulSoup 
import json
import os

def extract(ancestor, selector=None, attribute=None, return_list=False):
    if return_list:
        if attribute:
            return [tag[attribute].strip() for tag in ancestor.select(selector)]
        return [tag.text.strip() for tag in ancestor.select(selector)]   
    if selector:
        if attribute:
            try:
                return ancestor.select_one(selector)[attribute].strip()
            except:
                return None
        try:
            return ancestor.select_one(selector).text.strip()
        except:
            return None
    if attribute:
        try:
            return ancestor[attribute].strip()
        except:
            return None
    return ancestor.text.strip()

selectors = {
    "opinion_id": [None,"data-entry-id"],
    "author": ["span.user-post__author-name"],
    "recommend": ["span.user-post__author-recomendation > em"],
    "stars": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "cons": ["div.review-feature__title--negatives ~ div.review-feature__item", None, True],
    "pros": ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
    "opinion_date": ["span.user-post__published > time:nth-child(1)","datetime"],
    "purchase_date": ["span.user-post__published > time:nth-child(2)","datetime"],
    "up_vote": ["button.vote-yes","data-total-vote"],
    "down_vote": ["button.vote-no","data-total-vote"],
}

#id = '97863463' #iphone
id = '157286185' #lenovo
CeneoUrl = 'https://www.ceneo.pl/'
url = CeneoUrl + id + '#tab=reviews'
print(url)
all_opinions = []
NextPage = True
while NextPage:
    http = re.get(url)

    code = BeautifulSoup(http.text,"html.parser")

    opinions = code.select("div.js_product-review")

    for x in opinions:
        single_opinion = {
            key: extract(x, *value)
                for key, value in selectors.items()
        }
        all_opinions.append(single_opinion)
    arrow = code.select_one("a.pagination__next")
    if arrow:
        url = CeneoUrl + arrow["href"]
        print(arrow["href"])
    else:    
        NextPage = False


#print(all_opinions)

if not os.path.exists('opinions'):
    os.mkdir('opinions')

with open(f'opinions/{id}.json',"w",encoding="UTF-8") as js:
    json.dump(all_opinions,js,indent=4,ensure_ascii=False)