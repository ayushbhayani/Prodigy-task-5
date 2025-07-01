from flask import Flask, render_template, send_file
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
csv_file_path = "books_data.csv"

@app.route("/")
def index():
    return render_template("index.html", csv_ready=False)

@app.route("/scrape", methods=["POST"])
def scrape():
    products = []
    for page in range(1, 6):
        url = f"http://books.toscrape.com/catalogue/page-{page}.html"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        for book in books:
            name = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
            rating_class = book.find("p", class_="star-rating")["class"][1]
            rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}.get(rating_class, 0)
            products.append({"Name": name, "Price": price, "Rating": rating})
    pd.DataFrame(products).to_csv(csv_file_path, index=False)
    return render_template("index.html", csv_ready=True)

@app.route("/download")
def download_csv():
    return send_file(csv_file_path, as_attachment=True)

# ✅ THIS PART STARTS THE SERVER
if __name__ == "__main__":
    app.run(debug=True)
