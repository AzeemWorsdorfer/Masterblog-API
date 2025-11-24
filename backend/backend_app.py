import json
import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BLOG_POST_FILE = os.path.join(BASE_DIR, "posts.json")


def load_posts():
    """
    Loads blog posts from the JSON file.

    Returns:
        list: A list of blog post dictionaries. Returns an empty list on file error or absence.
    """
    if not os.path.exists(BLOG_POST_FILE) or os.path.getsize(BLOG_POST_FILE) == 0:
        return []

    try:
        with open(BLOG_POST_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(
            f"ERROR: Could not decode JSON from {BLOG_POST_FILE}. Check file format.")
        return []


def save_posts(posts):
    """
    Writes the current list of posts back to the JSON file.

    Args:
        posts (list): The list of blog post dictionaries to save.
    """
    try:
        # Use json.dump to write directly to the file object
        with open(BLOG_POST_FILE, "w") as f:
            json.dump(posts, f, indent=4)
        print(
            f"INFO: Successfully saved {len(posts)} posts to {BLOG_POST_FILE}.")
    except Exception as e:
        print(f"ERROR: Failed to save posts to {BLOG_POST_FILE}: {e}")


def get_next_id():
    """
    Generates the next sequential ID for a new blog post.
    Finds the highest existing ID in the global POSTS list and adds 1.
    """
    if not POSTS:
        return 1

    max_id = max(post.get('id', 0) for post in POSTS)
    return max_id + 1


# Load all posts into a global variable POSTS at startup.
POSTS = load_posts()


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

    new_post['id'] = get_next_id()

    POSTS.append(new_post)

    save_posts(POSTS)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """ Deletes a blog post from the JSON."""
    post_to_delete = None
    for index, post in enumerate(POSTS):
        if post['id'] == post_id:
            post_to_delete = index
            break

    if post_to_delete is not None:
        del POSTS[post_to_delete]

        save_posts(POSTS)

        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200
    else:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """ Updates blog post from JSON. """
    
    updated_data = request.get_json()
    if not updated_data:
        pass 
        
    post_to_update = None
    for post in POSTS: 
        if post['id'] == post_id:
            post_to_update = post
            break

    if post_to_update is None: 
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    if 'title' in updated_data:
        post_to_update['title'] = updated_data['title']
    
    if 'content' in updated_data:
        post_to_update['content'] = updated_data['content']
        
    save_posts(POSTS) 
    return jsonify(post_to_update), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
