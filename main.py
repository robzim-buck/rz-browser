from flask import Flask, render_template, request, send_file, abort
import os
from pathlib import Path
import mimetypes

app = Flask(__name__)

# Configure the root directory that users can browse
# Change this to the directory you want to expose
# ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

ROOT_DIR = '/mnt/core/work/current/rztest'


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
        # return send_file(abs_path)
        parent_dir = os.path.dirname(abs_path)
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>File Path</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                .path {{ background: #f4f4f4; padding: 15px; border-radius: 5px; word-break: break-all; margin-bottom: 20px; }}
                .back-btn {{ padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
                .back-btn:hover {{ background: #0056b3; }}
            </style>
        </head>
        <body>
            <h2>File Path</h2>
            <div class="path"><code>{abs_path}</code></div>
            <a href="/browse?path={parent_dir}" class="back-btn">← Back</a>
        </body>
        </html>
        '''

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
    app.run(debug=True, port=8000, host='0.0.0.0')
