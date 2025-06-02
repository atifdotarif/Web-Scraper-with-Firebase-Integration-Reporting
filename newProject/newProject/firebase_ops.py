import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_to_firebase(data_list):
    for data in data_list:
        if data['product_id'] is not None:
            doc_id = data["product_id"]
            db.collection("products").document(doc_id).set(data)

def fetch_from_firebase():
    docs = db.collection("products").stream()
    return {doc.id: doc.to_dict() for doc in docs}
