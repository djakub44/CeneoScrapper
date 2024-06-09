

import requests as re
from bs4 import BeautifulSoup 
import json
import os
import pandas as pd
import numpy as np 
import matplotlib as plot
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


if __name__ == "__main__":
    #id = '97863463' #iphone
    #id = '157286185' #lenovo
    #id = '56046405' #bosch
    id = '151210226' #tv

    CeneoUrl = 'https://www.ceneo.pl/'
    url = CeneoUrl + id + '#tab=reviews'
    #print(url)
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
            #print(arrow["href"])
        else:    
            NextPage = False


    #print(all_opinions)

    if not os.path.exists('opinions'):
        os.mkdir('opinions')

    with open(f'opinions/{id}.json',"w",encoding="UTF-8") as js:
        json.dump(all_opinions,js,indent=4,ensure_ascii=False)


        #wyswietlenie listy id
    print ('\n'.join(file.split(".")[0] for file in os.listdir("opinions")))

        
        #wczytanie kodu produktu o ktorum maja zostac przeanalizowane opinie
    #product_id = input("product id: ")
    product_id = id
    opinions = pd.read_json(f"opinions/{product_id}.json")
    opinions.stars = opinions.stars.apply(lambda s: s.split("/")[0].replace(",",".")).astype(float)


        #podstawowe statystyki
    opinions_count = len(opinions)
    pros_count = opinions.pros.astype(bool).sum() 
    cons_count = opinions.cons.astype(bool).sum() 
    average_stars = opinions.stars.mean()

        #histogram czestosci ocen

    stars_distribution = opinions.stars.value_counts().reindex(np.arange(0,5.5,0.5)) #od 0 do 5.0 z krokiem 0.5
    ax = stars_distribution.plot.bar(color="lightskyblue")
    ax.bar_label(ax.containers[0],label_type='edge',fmt=lambda l: int(l) if l >0 else "")
    ax.set_title(f'Histogram czestosci ocen w opiniach o {product_id}')
    ax.set_ylabel("Liczba gwiazdek")
    ax.set_xlabel("Liczba opinii")
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
    #plot.pyplot.show()

        #wykres udzialu rekomendacji w opiniach
    ax.clear()
    
    recomendations_distribution = opinions.recommend.value_counts(dropna=False).reindex(["Polecam","Nie polecam",np.NAN])
    bx = recomendations_distribution.plot.pie(
        #autopct="%1.1f%%"
        autopct=lambda s: f'{s:1.1f}%' if s>0 else "",
        label="",
        title=f"Udzial rekomendacji w opiniach o produkcie {product_id}",
        colors=["forestgreen","red","gray"],
        labels=["Polecam","Nie Polecam", "Nie mam zdania"]
    )

    plot.pyplot.show()