# import requests
# from bs4 import BeautifulSoup
# import json
# from pymongo import MongoClient
# from datetime import datetime

# # Headers to mimic a real browser and avoid bot detection
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Accept-Encoding": "gzip, deflate, br",
# }

# # MongoDB connection (same as your FastAPI app)
# client = MongoClient('mongodb://localhost:27017')
# db = client['scraper_db']
# products_collection = db['products']  # New collection for scraped products

# def scrape_walmart_product(url):
#     try:
#         # Send HTTP request to Walmart product page
#         response = requests.get(url, headers=HEADERS)
#         response.raise_for_status()  # Check for request errors

#         # Parse HTML with BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Find the __NEXT_DATA__ script tag containing JSON data
#         next_data_script = soup.find('script', id='__NEXT_DATA__')
#         if not next_data_script:
#             raise ValueError("Could not find __NEXT_DATA__ script tag")

#         # Extract and parse JSON data
#         json_data = json.loads(next_data_script.text)
#         product_data = json_data['props']['pageProps']['initialData']['data']['product']

#         # Extract relevant product details
#         scraped_product = {
#             'product_id': product_data.get('id', 'N/A'),  # Walmart product ID
#             'name': product_data.get('name', 'N/A'),  # Product name
#             'price': product_data.get('priceInfo', {}).get('currentPrice', {}).get('price', 'N/A'),  # Current price
#             'description': product_data.get('shortDescription', 'N/A'),  # Short description
#             'rating': product_data.get('averageRating', 'N/A'),  # Average rating
#             'num_reviews': product_data.get('totalReviewCount', 'N/A'),  # Number of reviews
#             'url': url,
#             'scraped_at': datetime.utcnow()
#         }

#         # Save to MongoDB
#         products_collection.insert_one(scraped_product)
#         print(f"Successfully scraped and saved product: {scraped_product['name']}")

#         return scraped_product

#     except Exception as e:
#         print(f"Error scraping {url}: {str(e)}")
#         return None

# def main():
#     # Example Walmart product URL (replace with any Walmart product URL)
#     product_url = "https://www.walmart.com/ip/Logitech-MX-Master-3S-Wireless-Performance-Mouse-Ergo-8K-DPI-Quiet-Clicks-USB-C-Black/731473988"
    
#     # Scrape the product
#     result = scrape_walmart_product(product_url)
    
#     if result:
#         # Print the scraped data
#         print("\nScraped Product Data:")
#         print(json.dumps(result, indent=2, default=str))

# if __name__ == "__main__":
#     main()


























# import requests
# from bs4 import BeautifulSoup
# import json
# from pymongo import MongoClient
# from datetime import datetime

# # Headers to mimic a real browser and avoid bot detection
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Accept-Encoding": "gzip, deflate, br",
# }

# # MongoDB connection (same as your FastAPI app)
# client = MongoClient('mongodb://localhost:27017/')
# db = client['scraper_db']
# products_collection = db['products']  # Collection for scraped products

# def scrape_walmart_product(url):
#     try:
#         # Create initial product entry with status 'pending'
#         product = {
#             'product_id': 'N/A',  # Will be updated after scraping
#             'name': 'N/A',
#             'price': 'N/A',
#             'description': 'N/A',
#             'rating': 'N/A',
#             'url': url,
#             'status': 'pending',
#             'scraped_at': datetime.utcnow()
#         }
#         # Insert the initial product entry into MongoDB and get its ID
#         result = products_collection.insert_one(product)
#         product_id = result.inserted_id

#         # Send HTTP request to Walmart product page
#         response = requests.get(url, headers=HEADERS)
#         response.raise_for_status()  # Check for request errors

#         # Parse HTML with BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Find the __NEXT_DATA__ script tag containing JSON data
#         next_data_script = soup.find('script', id='__NEXT_DATA__')
#         if not next_data_script:
#             raise ValueError("Could not find __NEXT_DATA__ script tag")

#         # Extract and parse JSON data
#         json_data = json.loads(next_data_script.text)
#         product_data = json_data['props']['pageProps']['initialData']['data']['product']

#         # Update product details
#         scraped_product = {
#             'product_id': product_data.get('id', 'N/A'),  # Walmart product ID
#             'name': product_data.get('name', 'N/A'),  # Product name
#             'price': product_data.get('priceInfo', {}).get('currentPrice', {}).get('price', 'N/A'),  # Current price
#             'description': product_data.get('shortDescription', 'N/A'),  # Short description
#             'rating': product_data.get('averageRating', 'N/A'),  # Average rating
#             'url': url,
#             'status': 'completed',  # Update status to completed
#             'scraped_at': datetime.utcnow()
#         }

#         # Update the product in MongoDB with scraped data and completed status
#         products_collection.update_one(
#             {'_id': product_id},
#             {'$set': scraped_product}
#         )
#         print(f"Successfully scraped and saved product: {scraped_product['name']}")

#         return scraped_product

#     except Exception as e:
#         # Update status to failed if an error occurs
#         products_collection.update_one(
#             {'_id': product_id},
#             {
#                 '$set': {
#                     'status': 'failed',
#                     'error': str(e),
#                     'scraped_at': datetime.utcnow()
#                 }
#             }
#         )
#         print(f"Error scraping {url}: {str(e)}")
#         return None

# def main():
#     # Example Walmart product URL (replace with any Walmart product URL)
#     product_url = "https://www.walmart.com/ip/Logitech-MX-Master-3S-Wireless-Performance-Mouse-Ergo-8K-DPI-Quiet-Clicks-USB-C-Black/731473988"
    
#     # Scrape the product
#     result = scrape_walmart_product(product_url)
    
#     if result:
#         # Print the scraped data
#         print("\nScraped Product Data:")
#         print(json.dumps(result, indent=2, default=str))

# if __name__ == "__main__":
#     main()


















# import requests
# from bs4 import BeautifulSoup
# import json
# from pymongo import MongoClient
# from datetime import datetime

# # Headers for web scraping
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Accept-Encoding": "gzip, deflate, br",
# }

# # MongoDB connection
# client = MongoClient('mongodb://localhost:27017')
# db = client['scraper_db']
# products_collection = db['products']

# def scrape_walmart_product(url):
#     document_id = None  # in case exception fires before insert
#     try:
#         # Pehle ek "pending" status waala document dal do
#         pending_product = {
#             'url': url,
#             'status': 'pending',
#             'scraped_at': datetime.utcnow()
#         }
#         result = products_collection.insert_one(pending_product)
#         document_id = result.inserted_id

#         # Webpage scrape karo
#         response = requests.get(url, headers=HEADERS, timeout=10)
#         response.raise_for_status()

#         soup = BeautifulSoup(response.text, 'html.parser')
#         next_data_script = soup.find('script', id='__NEXT_DATA__')
#         if not next_data_script:
#             raise ValueError("Could not find __NEXT_DATA__ script tag")

#         json_data = json.loads(next_data_script.text)
#         product_data = json_data['props']['pageProps']['initialData']['data']['product']

#         updated_product = {
#             'product_id': product_data.get('id', 'N/A'),
#             'name': product_data.get('name', 'N/A'),
#             'price': product_data.get('priceInfo', {}).get('currentPrice', {}).get('price', 'N/A'),
#             'description': product_data.get('shortDescription', 'N/A'),
#             'rating': product_data.get('averageRating', 'N/A'),
#             'url': url,
#             'status': 'completed',
#             'scraped_at': datetime.utcnow()
#         }

#         products_collection.update_one(
#             {'_id': document_id},
#             {'$set': updated_product}
#         )
#         print(f"Successfully scraped: {updated_product['name']}")
#         return updated_product

#     except Exception as e:
#         # Error aayi toh status=failed likhdo aur error bhi save karo
#         if document_id is not None:
#             products_collection.update_one(
#                 {'_id': document_id},
#                 {'$set': {'status': 'failed', 'error': str(e), 'scraped_at': datetime.utcnow()}}
#             )
#         print(f"Error scraping {url}: {str(e)}")
#         return None

# # ---------- TEST KARNE KE LIYE (EXAMPLE) ----------
# # Niche wala block sirf jab aap script run karna chaho tabhi rakho, warna hata do

# if __name__ == "__main__":
#     product_url = "https://www.walmart.com/ip/Logitech-MX-Master-3S-Wireless-Performance-Mouse-Ergo-8K-DPI-Quiet-Clicks-USB-C-Black/731473988"
#     result = scrape_walmart_product(product_url)
#     if result:
#         print("Scraped Product Data:")
#         print(json.dumps(result, indent=2, default=str))


















































import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from datetime import datetime

# Headers to mimic browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['scraper_db']
products_collection = db['products']

def scrape_walmart_product(url):
    document_id = None
    try:
        print(f"Starting scrape for URL: {url}")

        # Insert pending record first
        pending_product = {
            'url': url,
            'status': 'pending',
            'scraped_at': datetime.utcnow()
        }
        result = products_collection.insert_one(pending_product)
        document_id = result.inserted_id
        print(f"Inserted pending product with ID: {document_id}")

        # Get page content
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        print("Fetched page successfully")

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        next_data_script = soup.find('script', id='__NEXT_DATA__')
        if not next_data_script:
            raise ValueError("Could not find __NEXT_DATA__ script tag!")
        print("__NEXT_DATA__ script tag found")

        # Parse JSON from script tag
        json_data = json.loads(next_data_script.string)
        print("Parsed JSON data")

        # Navigate JSON structure 
        product_data = json_data['props']['pageProps']['initialData']['data']['product']
        print(f"Product data extracted: {product_data.get('name', 'N/A')}")

        # Prepare update dict
        updated_product = {
            'product_id': product_data.get('id', 'N/A'),
            'name': product_data.get('name', 'N/A'),
            'price': product_data.get('priceInfo', {}).get('currentPrice', {}).get('price', 'N/A'),
            'description': product_data.get('shortDescription', 'N/A'),
            'rating': product_data.get('averageRating', 'N/A'),
            'url': url,
            'status': 'completed',
            'scraped_at': datetime.utcnow()
        }

        # Update the document in DB
        products_collection.update_one({'_id': document_id}, {'$set': updated_product})
        print(f"Product data updated successfully in DB for ID: {document_id}")
        return updated_product

    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        if document_id is not None:
            products_collection.update_one(
                {'_id': document_id},
                {'$set': {'status': 'failed', 'error': str(e), 'scraped_at': datetime.utcnow()}}
            )
        return None


# Testing block
if __name__ == '__main__':
    # Example 
    test_url = "https://www.walmart.com/ip/Logitech-MX-Master-3S-Wireless-Performance-Mouse-Ergo-8K-DPI-Quiet-Clicks-USB-C-Black/731473988"
    product = scrape_walmart_product(test_url)
    if product:
        print("\nScraped Product Data:")
        print(json.dumps(product, indent=2, default=str))














