import amazon_paapi
from amazon_paapi import AmazonApi
from process_image import process_image

ACCESS_KEY = "your-access-key"
SECRET_KEY = "your-secret-key"
PARTNER_TAG = "your-associate-tag"
api = AmazonApi(
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    partner_tag=PARTNER_TAG,
    country="IN"
)
def search_amazon_from_image(img_file):
    detected_object = process_image(img_file)
    if detected_object:
        print(f"Detected object: {detected_object}")
        try:
            search_results = api.search_items(keywords=detected_object, search_index="All")
            for item in search_results['Items']:
                title = item['ItemInfo']['Title']['DisplayValue']
                url = item['DetailPageURL']
                price = item['Offers']['Listings'][0]['Price'][
                    'DisplayAmount'] if 'Offers' in item else "Price not available"

                print(f"Title: {title}")
                print(f"Price: {price}")
                print(f"URL: {url}\n")
        except amazon_paapi.exceptions.PAAPIException as e:
            print(f"An error occurred: {e}")
    else:
        print("No object detected in the image.")
