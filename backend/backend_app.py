import json
import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

# --- CONFIGURATION ---
app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_POST_FILE = os.path.join(BASE_DIR, "posts.json")

# --- DATA ACCESS HELPERS ---


def load_posts():
    """
    Loads blog posts from the JSON file with UTF-8 encoding.
    """
    # Check if file exists and is not empty
    if not os.path.exists(BLOG_POST_FILE) or os.path.getsize(BLOG_POST_FILE) == 0:
        return []

    try:
        with open(BLOG_POST_FILE, "r", encoding="utf8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(
            f"ERROR: Could not decode JSON from {BLOG_POST_FILE}. Check file format.")
        return []
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while loading posts: {e}")
        return []


def save_posts(posts):
    """
    Writes the current list of posts back to the JSON file with UTF-8 encoding.
    """
    try:

        with open(BLOG_POST_FILE, "w", encoding="utf8") as f:
            json.dump(posts, f, indent=4)
        print(
            f"INFO: Successfully saved {len(posts)} posts to {BLOG_POST_FILE}.")
    except Exception as e:
        print(f"ERROR: Failed to save posts to {BLOG_POST_FILE}: {e}")


def get_next_id(current_posts):
    """
    Generates the next sequential ID for a new blog post.
    Accepts the current list of posts instead of using a global.
    """
    if not current_posts:
        return 1

    # Use current_posts instead of a global POSTS
    max_id = max(post.get('id', 0) for post in current_posts)
    return max_id + 1


# --- SWAGGER CONFIGURATION (No change needed here) ---
SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# --- API ROUTES ---


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """ Gets all blog posts in JSON Format, with optional sorting."""

    posts_data = load_posts()

    sort_field = request.args.get('sort')
    direction = request.args.get('direction')

    posts_to_return = list(posts_data)

    VALID_SORT_FIELDS = ['title', 'content']
    VALID_DIRECTIONS = ['asc', 'desc']

    if sort_field:

        if sort_field not in VALID_SORT_FIELDS:
            return jsonify({"error": f"Invalid sort field: {sort_field}. Must be one of {VALID_SORT_FIELDS}."}), 400

        if direction not in VALID_DIRECTIONS:
            return jsonify({"error": f"Invalid sort direction: {direction}. Must be one of {VALID_DIRECTIONS}."}), 400

        reverse_sort = direction == 'desc'

        try:
            posts_to_return.sort(
                key=lambda post: post[sort_field], reverse=reverse_sort)
        except KeyError:
            return jsonify({"error": f"Internal error: Post missing required field for sorting."}), 500

    return jsonify(posts_to_return)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """ Searches posts by title or content using query parameters. """

    posts_data = load_posts()

    search_title = request.args.get('title')
    search_content = request.args.get('content')

    if not search_title and not search_content:
        return jsonify(posts_data)  # Return all if no search params

    results = []

    search_title_lower = search_title.lower() if search_title else None
    search_content_lower = search_content.lower() if search_content else None

    for post in posts_data:
        title_matches = False
        content_matches = False

        if search_title_lower and search_title_lower in post.get('title', '').lower():
            title_matches = True

        if search_content_lower and search_content_lower in post.get('content', '').lower():
            content_matches = True

        if title_matches or content_matches:
            results.append(post)

    return jsonify(results)


@app.route('/api/posts', methods=['POST'])
def add_posts():
    """ Adds a blog post to the JSON list of posts."""

    posts_data = load_posts()

    new_post = request.get_json()
    if not new_post or not new_post.get('title') or not new_post.get('content'):
        return jsonify({"Error": "Title and Content are required!"}), 400

    # Pass posts_data to get_next_id
    new_post['id'] = get_next_id(posts_data)

    posts_data.append(new_post)

    # Pass updated posts_data to save_posts
    save_posts(posts_data)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """ Deletes a blog post from the JSON."""

    posts_data = load_posts()

    post_index_to_delete = None
    for index, post in enumerate(posts_data):
        if post['id'] == post_id:
            post_index_to_delete = index
            break

    if post_index_to_delete is not None:
        del posts_data[post_index_to_delete]

        # Pass updated posts_data to save_posts
        save_posts(posts_data)

        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200
    else:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """ Updates blog post from JSON. """

    posts_data = load_posts()

    updated_data = request.get_json()

    post_to_update = None
    for post in posts_data:
        if post['id'] == post_id:
            post_to_update = post
            break

    if post_to_update is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    if 'title' in updated_data:
        post_to_update['title'] = updated_data['title']

    if 'content' in updated_data:
        post_to_update['content'] = updated_data['content']
save_posts(posts_data)
    return jsonify(post_to_update), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
