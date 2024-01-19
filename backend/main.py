from flask import Flask
import os
from mongo_connector import get_db, data_init, clear_collections, get_collections_data

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://talkmemo:talkmemo@cluster0.ki1vh64.mongodb.net/?retryWrites=true&w=majority"
app.config['MONGO_DB'] = "talkmemo"

@app.route('/')
def hello():
    return 'Hello, this is your Flask backend!'

@app.route('/get')
def get_all_data():
    json_data = get_collections_data()
    return json_data

@app.route('/init')
def init():
    data_init()
    return "data initiated"

@app.route('/clear')
def clear():
    clear_collections()
    return "collections cleared"

if __name__ == '__main__':
    # Check if running locally or on App Engine
    if os.getenv('GAE_ENV') != 'standard':
        # If running locally, use a specific port
        app.run(debug=True, port=8080)
    else:
        # If running on App Engine, use the dynamically assigned port
        app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
