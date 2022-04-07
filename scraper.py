import requests
from bs4 import BeautifulSoup
import json


url = "https://www.ceneo.pl/95365253#tab=reviews"


all_reviews = []
while(url):
    response = requests.get(url)
    page_dom = BeautifulSoup(response.text, 'html.parser')
    reviews = page_dom.select("div.js_product-review")
    for review in reviews:
        review_id = review["data-entry-id"]
        author = review.select_one("span.user-post__author-name").text.strip()
        try:
            recommendation = review.select_one("span.user-post__author-recomendation > em").text.strip()
            recommendation = True if recommendation == "Polecam" else False 
        except AttributeError: recommendation = None
        stars = review.select_one("span.user-post__score-count").text.strip()
        stars = float(stars.split("/").pop(0).replace(",", "."))
        content = review.select_one("div.user-post__text").text.strip()
        publish_date = review.select_one("span.user-post__published > time:nth-child(1)")["datetime"]
        try:
            purchase_date = review.select_one("span.user-post__published > time:nth-child(2)")["datetime"]
        except TypeError: purchase_date = None
        useful = review.select_one("button.vote-yes > span").text.strip()
        useful = int(useful)
        useless = review.select_one("button.vote-no > span").text.strip()
        useless = int(useless)
        pros = review.select("div.review-feature__title--positives ~ div.review-feature__item")
        pros = [item.text.strip() for item in pros]
        cons = review.select("div.review-feature__title--negatives ~ div.review-feature__item")
        cons = [item.text.strip() for item in cons]

        single_review = {
            "review_id": review_id, 
            "author": author,
            "recommendation": recommendation,
            "stars": stars,
            "content": content,
            "publish_date": publish_date,
            "purchase_date": purchase_date, 
            "useful": useful, 
            "useless": useless,
            "pros": pros,
            "cons": cons
        }
        all_reviews.append(single_review)

    try: 
        next_page = page_dom.select_one("a.pagination__next")
        url = "https://www.ceneo.pl"+next_page["href"]
    except TypeError: url = None

with open("./reviews/103475515.json", "w", encoding="UTF-8") as f:
    json.dump(all_reviews, f, indent=4, ensure_ascii=False)