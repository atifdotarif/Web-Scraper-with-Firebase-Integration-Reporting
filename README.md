# Web-Scraper-with-Firebase-Integration-Reporting

Approach:
Used Scrapy to crawl product listings from the Junaid Jamshed men's Kameez Shalwar category. The spider extracts key product details like name, price, product ID, image URL, and link.

The scraped data is stored in Firebase Firestore using the product_id as the document ID to uniquely identify each product. This prevents duplication.


To avoid updating Firebase with identical data every time the spider runs, the Firebase upload is disabled by default in the spider's pipeline. So data is being updated in firebase database on running comparer.py, after comparison. the scraper just save new data latest_data.py. Then on running comparer.py compares that new data firebase data of previous snapshot.

A separate script comparer.py compares the latest scraped data (latest_products.json) with existing data in Firebase:
Detects new products, products with increased and decreased prices  
Generates comparison_report.txt

Uploads the updated data snapshot to Firebase if changes are found
