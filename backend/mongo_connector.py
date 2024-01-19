from datetime import datetime
import json
import random
from pymongo.mongo_client import MongoClient
from flask import current_app, g

MONGO_URI = "mongodb+srv://talkmemo:talkmemo@cluster0.ki1vh64.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB = "talkmemo"

def get_db():
    """
    Get the MongoDB connection from the Flask application context.
    """

    if 'db' not in g:
        client = MongoClient(MONGO_URI)
        g.db = client[MONGO_DB]


    return g.db

def create_db():

    db = get_db()

    collections = [
        {'name': 'User', 'fields': ['id', 'name', 'password', 'isVIP']},
        {'name': 'Notice', 'fields': ['id', 'user_id', 'time', 'text']},
        {'name': 'Upload', 'fields': ['id', 'user_id', 'url', 'type', 'time', 'indexes']},
        {'name': 'Notes', 'fields': ['id', 'user_id', 'time', 'text']},
        {'name': 'NoteToSentence', 'fields': ['id', 'note_id', 'text', 'translation']},
        {'name': 'NoteStared', 'fields': ['note_id', 'user_id']},
        {'name': 'UserNotes', 'fields': ['note_id', 'user_id']}
    ]

    for collection_info in collections:
        collection_name = collection_info['name']
        fields = collection_info['fields']

        if collection_name not in db.list_collection_names():
            collection = db[collection_name]
            collection.create_index('id', unique=True)

            for field in fields:
                if field != 'id':
                    collection.create_index(field)

    print("Collections created or already existed.")

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
    stared_notes_collection.insert_many([
        {'note_id': note['id'], 'user_id': 1} for note in stared_notes_data
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

def get_collections_data():

    db = get_db()

    # Collections to retrieve data from
    collections_to_export = ['User', 'Notice', 'Upload', 'Notes', 'NoteToSentence', 'NoteStared', 'UserNotes']

    data = {}

    for collection_name in collections_to_export:
        collection = db[collection_name]
        cursor = collection.find({})

        collection_data = [document for document in cursor]

        data[collection_name] = collection_data

    json_data = json.dumps(data, default=str, indent=2)


    return json_data
