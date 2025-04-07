from flask import Flask, render_template, request, send_file, abort
import os
from pathlib import Path
import mimetypes

app = Flask(__name__)

# Configure the root directory that users can browse
# Change this to the directory you want to expose
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


@app.route('/')
def index():
    return browse(ROOT_DIR)


@app.route('/browse')
def browse_path():
    requested_path = request.args.get('path', ROOT_DIR)
    return browse(requested_path)


def browse(path):
    # Security check: ensure the path is within the ROOT_DIR
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(ROOT_DIR):
        abort(403)  # Forbidden

    if not os.path.exists(abs_path):
        abort(404)  # Not found

    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # List the directory contents
    items = []
    for item in os.listdir(abs_path):
        item_path = os.path.join(abs_path, item)
        item_type = "dir" if os.path.isdir(item_path) else "file"
        items.append({
            "name": item,
            "path": item_path,
            "type": item_type
        })

    # Sort directories first, then files
    items.sort(key=lambda x: (0 if x["type"] == "dir" else 1, x["name"].lower()))

    parent_dir = os.path.dirname(abs_path) if abs_path != ROOT_DIR else None

    return render_template('browse.html', 
                          items=items, 
                          current_path=abs_path,
                          parent_dir=parent_dir,
                          root_dir=ROOT_DIR)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
