from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    direction = request.args.get('direction')

    sorted_posts = POSTS.copy()

    if sort_field and sort_field in ['title', 'content']:
        if direction == 'asc':
            sorted_posts.sort(key=lambda post: post[sort_field])
        elif direction == 'desc':
            sorted_posts.sort(key=lambda post: post[sort_field], reverse=True)
        else:
            return jsonify({"error": "Invalid direction parameter. Valid values are 'asc' and 'desc'."}), 400

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def create_post():
    # Get the new Post
    data = request.get_json()

    # Check if title and content are provided
    if "title" not in data or "content" not in  data:
        return jsonify({"error": "Title and content are required."}), 400

    # Create a new post wint an automatically generated ID
    new_post = {
        "id": len(POSTS) + 1,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201


def find_post_index(id):
    for i, post in enumerate(POSTS):
        if post["id"] == id:
            return i
    return None


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global POSTS
    # Find the Post with the given ID
    post_index = find_post_index(id)

    # If the post was found, delete it
    if post_index is not None:
        deleted_post = POSTS.pop(post_index)
        return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200

    else:
        return jsonify({"error": f"Post with id {id} not found."}), 404


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    global POSTS

    # Find the Post with the given ID
    post_index = find_post_index(id)

    # If the post was found, update it
    if post_index is not None:
        post = POSTS[post_index]
        data = request.get_json()
        title = data.get("title", post["title"])
        content = data.get("content", post["content"])
        post["title"] = title
        post["content"] = content
        return  jsonify(post), 200

    else:
        return jsonify({"error": f"Post with id {id} not found."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title')
    content = request.args.get('content')

    if not title and not content:
        return jsonify([])

    matched_posts = []

    for post in POSTS:
        if title and title.lower() in post["title"].lower():
            matched_posts.append(post)
        if content and content.lower() in post["content"].lower():
            matched_posts.append(post)

    return jsonify(matched_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
