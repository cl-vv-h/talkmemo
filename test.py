from datetime import datetime
import random
from pymongo.mongo_client import MongoClient

client = MongoClient("mongodb+srv://talkmemo:talkmemo@cluster0.ki1vh64.mongodb.net/?retryWrites=true&w=majority")
db = client["talkmemo"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

MONGO_URI = "mongodb+srv://talkmemo:talkmemo@cluster0.ki1vh64.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB = "talkmemo"

def get_db():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


    return db

def data_init():
    def random_date(start_date, end_date):
        return start_date + (end_date - start_date) * random.random()

    db = get_db()

    # User data
    user_data = {
        'id': 1,
        'name': 'John Doe',
        'password': 'hashed_password',  # You should use a secure hashing algorithm
        'isVIP': True
    }

    print(db.list_collection_names())
    # Insert user into 'User' collection
    user_collection = db['User']
    user_collection.replace_one({'id': 1}, user_data, upsert=True)

    # Generate realistic notes data
    notes_data = [
        {'id': i, 'user_id': 1, 'time': random_date(datetime(2022, 1, 1), datetime.now()), 'text': f'Note {i} content'}
        for i in range(1, 11)
    ]

    # Insert notes into 'Notes' collection
    notes_collection = db['Notes']
    notes_collection.insert_many(notes_data)

    # Randomly choose 2 notes to be stared
    stared_notes_data = random.sample(notes_data, 2)

    # Insert stared notes into 'NoteStared' collection
    stared_notes_collection = db['NoteStared']
    stared_notes_collection.delete_many({})  # Clear existing data

    stared_notes_collection.insert_many([
        {'note_id': note['id'], 'user_id': 1, 'id': i + 1} for i, note in enumerate(stared_notes_data)
    ])

    # Generate sentences for each note
    note_to_sentence_data = []
    id = 1
    for note in notes_data:
        sentences = [
            {'note_id': note['id'], 'text': f'Sentence {i + 1} for Note {note["id"]}', 'translation': f'Translation {i + 1}', 'id': id+i}
            for i in range(2)
        ]
        id += 2
        note_to_sentence_data.extend(sentences)

    # Insert sentences into 'NoteToSentence' collection
    note_to_sentence_collection = db['NoteToSentence']
    note_to_sentence_collection.delete_many({})  # Clear existing data
    note_to_sentence_collection.insert_many(note_to_sentence_data)

    print("Realistic data inserted into MongoDB.")

def clear_collections():
    db = get_db()

    # Collections to clear
    collections_to_clear = ['User', 'Notice', 'Upload', 'Notes', 'NoteToSentence', 'NoteStared', 'UserNotes']

    for collection_name in collections_to_clear:
        collection = db[collection_name]
        collection.delete_many({})  # Remove all documents from the collection

    print("All data cleared from MongoDB collections.")


clear_collections()
data_init()