from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

# Sample data (in-memory database for simplicity)
books = [
    { "id": 1, "title": "Teenage Mutant Ninja Turtles x Naruto", "author": "Caleb Goellner", "image_url": "https://m.media-amazon.com/images/I/91iA+EfedXL._SY466_.jpg", "price": 15.80 },
    { "id": 2, "title": "Tim Burton's The Nightmare Before Christmas - Zero's Journey", "author": "D.J. Milky", "image_url": "https://m.media-amazon.com/images/I/71p8+8b6XzL._SY466_.jpg", "price": 24.99 },
    { "id": 3, "title": "One Piece, Vol. 1: Romance Dawn", "author": "Eiichiro Oda", "image_url": "https://m.media-amazon.com/images/I/91NxYvUNf6L._SY466_.jpg", "price": 7.68 },
    { "id": 4, "title": "Jujutsu Kaisen, Vol. 1", "author": "Gege Akutami", "image_url": "https://m.media-amazon.com/images/I/81TmHlRleJL._SY466_.jpg", "price": 7.18 },
    { "id": 5, "title": "Demon Slayer: Kimetsu no Yaiba, Vol. 1", "author": "Koyoharu Gotouge", "image_url": "https://m.media-amazon.com/images/I/81ZNkhqRvVL._SY466_.jpg", "price": 6.92 },
    { "id": 6, "title": "Spy x Family, Vol. 2", "author": "Tatsuya Endo", "image_url": "https://m.media-amazon.com/images/I/41Vpj9KnOaL._SY445_SX342_.jpg", "price": 9.99 },
    { "id": 7, "title": "Goodnight Punpun, Vol.1", "author": "Inio Asano", "image_url": "https://m.media-amazon.com/images/I/917IJDfk36L._SY425_.jpg", "price": 13.46 },
    { "id": 8, "title": "Solo Leveling, Vol. 1", "author": "Chugong", "image_url": "https://m.media-amazon.com/images/I/816hywlmu-L._SY425_.jpg", "price": 11.99 }
    ];

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS']='Content-Type'

# Set up JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Authentication endpoint to get JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    # In a real-world scenario, you would check the credentials against a database
    if username == 'user' and password == 'pass':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Create (POST) operation
@app.route('/books', methods=['POST'])
@cross_origin()
@jwt_required()
def create_book():
    data = request.get_json()

    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"],
        "image_url": data["image_url"]
    }

    books.append(new_book)
    return jsonify(new_book), 201

# Read (GET) operation - Get all books
@app.route('/books', methods=['GET'])
@cross_origin()
@jwt_required()
def get_all_books():
    return jsonify({"books": books})

# Read (GET) operation - Get a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
@cross_origin()
@jwt_required()
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Update (PUT) operation
@app.route('/books/<int:book_id>', methods=['PUT'])
@cross_origin()
@jwt_required()
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        data = request.get_json()
        book.update(data)
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404
    
# Delete operation
@app.route('/books/<int:book_id>', methods=['DELETE'])
@cross_origin()
@jwt_required()
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
