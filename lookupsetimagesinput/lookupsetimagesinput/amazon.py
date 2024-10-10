import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_amazon_product_link(product_name):
    search_url = "https://www.amazon.in/s?k=" + urllib.parse.quote({detected_object})
    headers = {
        "User-Agnt": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        product = soup.find("a", {"class": "a-link-normal", "href": True})
        if product:
            return product["href"]
        else:
            return "Product not found."
    else:
        return f"Failed to fetch results, status code: {response.status_code}"

product_name = "laptop"
product_link = get_amazon_product_link(product_name)
print("Product Link:", product_link)
