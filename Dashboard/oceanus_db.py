import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyBfTlFrewOca9OxubyqftNSqznTrJLWSlY",
    "authDomain": "oceanus-purpose.firebaseapp.com",
    "databaseURL": "https://oceanus-purpose-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "oceanus-purpose",
    "storageBucket": "oceanus-purpose.appspot.com",
    "messagingSenderId": "674501615782",
    "appId": "1:674501615782:web:ee6243a17663fe196e5467",
    "measurementId": "G-MDMB3N4508",
    "databaseURL": "https://oceanus-purpose-default-rtdb.europe-west1.firebasedatabase.app/"}

firebase = pyrebase.initialize_app(firebaseConfig)


def initialize_db():
    firebase_db = firebase.database()
    return firebase_db


def intialize_auth():
    firebase_auth = firebase.auth()
    return firebase_auth


def create_fake_data():
    db = initialize_db()
    data = {"name": "Palestinian", "timestamp": 1693486552.263934}
    for i in range(10):
        db.child("Raspberry Pi Data").child("Ships").child(data)
