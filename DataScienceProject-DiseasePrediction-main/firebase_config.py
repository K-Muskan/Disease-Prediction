import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate('C:\Shumail\Project\diseasepredictionsystematu-firebase-adminsdk-qwja1-503c907f96.json')
        firebase_admin.initialize_app(cred)
    return firestore.client()

# Initialize Firebase and get Firestore client
db = initialize_firebase()