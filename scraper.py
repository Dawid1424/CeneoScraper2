import requests
from bs4 import BeautifulSoup
import json

def extract_element(ancestor, selector, attribute=None, return_list=False):
    try:
        if attribute:
            return ancestor.select_one(selector)[attribute]
        elif return_list:
            return [item.text.strip() for item in ancestor.select(selector)]
        else:
            return ancestor.select_one(selector).text.strip()
    except (AttributeError, TypeError):
        return None

review_elements = {
    "author": ["span.user-post__author-name"],
    "recommendation": ["span.user-post__author-recomendation > em"],
    "stars": ["span.user-post__score-count"],
    "content": ["span.user-post__score-count"],
    "publish_date": ["span.user-post__published > time:nth-child(1)", "datetime"],
    "purchase_date": ["span.user-post__published > time:nth-child(2)", "datetime"], 
    "useful": ["button.vote-yes > span"], 
    "useless": ["button.vote-no > span"],
    "pros": ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
    "cons": ["div.review-feature__title--negatives ~ div.review-feature__item", None, True]
}
product_id = input("Podaj kod produktu")
url = f"https://www.ceneo.pl/{product_id}#tab=reviews"


all_reviews = []
while(url):
    response = requests.get(url)
    page_dom = BeautifulSoup(response.text, 'html.parser')
    reviews = page_dom.select("div.js_product-review")
    for review in reviews:
        single_opinion = {key:extract_element(review, *values)
                            for key, values in review_elements.items()}
        single_review["review_id"] = review["data-entry-id"]

        
        


        recommendation = True if recommendation == "Polecam" else False if single_review[recommendation] == "Nie polecam"
        single_review["stars"] = float(single_review["stars"].split("/").pop(0).replace(",", "."))
        single_review["useful"] = int(single_review["useful"])
        single_review["useless"] = int(single_review["useless"])
        


        all_reviews.append(single_review)

    try: 
        next_page = page_dom.select_one("a.pagination__next")
        url = "https://www.ceneo.pl"+next_page["href"]
    except TypeError: url = None

with open(f"./reviews/{product_id}.json", "w", encoding="UTF-8") as f:
    json.dump(all_reviews, f, indent=4, ensure_ascii=False)