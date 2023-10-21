from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name)


@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    google_url = f"https://www.google.com/search?q={keyword}&tbm=shop"

    response = requests.get(google_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the first shopping ad details
    shopping_ad = soup.find("div", class_="pla-unit")

    if shopping_ad:
        product_name = shopping_ad.find("h3").text
        price = shopping_ad.find("div", class_="Nr22bf").text
        image_url = shopping_ad.find("img")["src"]

        return render_template("result.html", product_name=product_name, price=price, image_url=image_url)
    else:
        return render_template("no_results.html", keyword=keyword)


if __name__ == "__main__":
    app.run()
