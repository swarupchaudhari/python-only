import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com"

response = requests.get(url)

print(response.status_code)



soup = BeautifulSoup(response.text, "html.parser")

print(soup.title.text)


books = soup.find_all("article", class_="product_pod")

print("Total Books:", len(books))





titles = []
prices = []

for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text

    titles.append(title)
    prices.append(price)

print(titles[:5])




data = {
    "Book Title": titles,
    "Price": prices
}

df = pd.DataFrame(data)

print(df.head())



df.to_csv("books_data.csv", index=False)

print("Dataset Saved Successfully!")




