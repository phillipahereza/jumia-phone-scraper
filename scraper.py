from bs4 import BeautifulSoup
import requests
import json


def get_phone(phone_div):
    sku = phone_div.get('data-sku')
    link_tag = phone_div.find('a', {'class': ["link"]})
    link = link_tag.get('href')
    img_tag = phone_div.find('img', {'class': ['lazy', 'image', '-loaded']})
    img_url = img_tag.get('data-src')
    brand = phone_div.find('span', {'class': ['brand']}).text
    name = phone_div.find('span', {'class': ['name']}).text
    price_container = phone_div.find('span', {'class': ['price']})
    price = price_container.find('span', {'dir': ['ltr']}).get('data-price')
    return {
        "brand": brand,
        "name": name,
        "sku": sku,
        "price": price,
        "link": link,
        "image": img_url
    }

    # result, _ = save_phone_to_db(brand=brand, image_url=img_url, name=name, price=price, sku=sku, link=link)

def save_phone_to_db(brand, image_url, name, price, sku, link):
    return True, {}

if __name__ == "__main__":
    results = []
    page_link = "https://www.jumia.ug/smartphones/"
    response = requests.get(page_link)

    soup = BeautifulSoup(response.content, 'html.parser')

    phone_divs = soup.find_all('div', {"class": ["sku", '-gallery']})
    for phone in phone_divs:
        results.append(get_phone(phone))
    

    pagination = soup.find('ul', {"class": "osh-pagination -horizontal"})
    max_page = max([int(i.text) for i in pagination.find_all('li') if i.text.isnumeric()])

    pages_to_scrape = [f"{page_link}?page={i}" for i in range(2, max_page+1)]

    for page in pages_to_scrape:
        print(f"{page}")
        response = requests.get(page)
        soup = BeautifulSoup(response.content, 'html.parser')
        phone_divs = soup.find_all('div', {"class": ["sku", '-gallery']})
        for phone in phone_divs:
            results.append(get_phone(phone))

    
    with open('phones.json', 'w') as f:
        json.dump(results, f)
        f.close()
