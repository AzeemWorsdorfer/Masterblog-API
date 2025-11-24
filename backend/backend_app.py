from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """ Gets all blog posts in JSON Format."""
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_posts():
    """ Adds a blog post to the JSON list of posts."""
    new_post = request.get_json()
    if not new_post.get('title') or not new_post.get('content'):
        return jsonify({"Error": "Title and Content are required!"}), 400

    new_post['id'] = len(POSTS) + 1
    POSTS.append(new_post)
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
