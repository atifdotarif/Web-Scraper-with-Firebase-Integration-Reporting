import json
from pathlib import Path
from newProject.firebase_ops import upload_to_firebase, fetch_from_firebase

def load_latest_scrape(json_path="latest_products.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_report():
    new_data = load_latest_scrape()
    old_data = fetch_from_firebase()

    old_data_dict = {doc_id: details for doc_id, details in old_data.items()}

    new_ids = {p["product_id"] for p in new_data}
    old_ids = set(old_data_dict.keys())

    new_products = new_ids - old_ids

    price_increased = []
    price_decreased = []
    out_of_stock = []

    for p in new_data:
        pid = p["product_id"]
        if pid in old_data_dict:
            old = old_data_dict[pid]
            if p["price"] > old["price"]:
                price_increased.append(pid)
            elif p["price"] < old["price"]:
                price_decreased.append(pid)
            if p["availability"].lower() == "out of stock":
                out_of_stock.append(pid)

    upload_to_firebase(new_data)

    report = f"""
J. Product Comparison Report
===============================

Products scraped: {len(new_data)}
New products: {len(new_products)}
 → Product IDs: {sorted(list(new_products))}

Price increased: {len(price_increased)}
 → Product IDs: {price_increased}

Price decreased: {len(price_decreased)}
 → Product IDs: {price_decreased}

Out of stock: {len(out_of_stock)}
 → Product IDs: {out_of_stock}
"""

    Path("report.txt").write_text(report, encoding="utf-8")
    print("Comparison complete. Saved to report.txt")

if __name__ == "__main__":
    generate_report()
