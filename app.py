from flask import Flask, request, jsonify
from pymongo import MongoClient
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['gasMonitoring']
collection = db['gas_analyze']

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.route('/update', methods=['PATCH'])
def update_entry():
    """
    Update the is_gas_leak and capacity fields for a given username.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            capacity:
              type: integer
    responses:
      200:
        description: Entry updated successfully
    """
    username = request.json['username']
    update_fields = {
        'capacity': request.json.get('capacity')
    }
    collection.update_one({'username': username}, {'$set': update_fields})
    return jsonify({"message": "Entry updated successfully"}), 200

@app.route('/reset', methods=['POST'])
def reset_entry():
    """
    Reset the is_gas_leak and capacity fields for a given username.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
    responses:
      200:
        description: Entry reset successfully
    """
    username = request.json['username']
    update_fields = {
        'is_gas_leak': False,
        'capacity': 100
    }
    result = collection.update_one({'username': username}, {'$set': update_fields})

    if result.matched_count == 0:
        return jsonify({"error": f"Username '{username}' not found"}), 404

    return jsonify({"message": "Entry reset successfully"}), 200

@app.route('/gas-update', methods=['PATCH'])
def update_gas_entry():
    """
    Update the is_gas_leak field for a given username.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            is_gas_leak:
              type: boolean
    responses:
      200:
        description: Entry updated successfully
    """
    username = request.json['username']
    update_fields = {
        'is_gas_leak': request.json.get('is_gas_leak')
    }
    collection.update_one({'username': username}, {'$set': update_fields})
    return jsonify({"message": "Entry updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
