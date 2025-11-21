import os
import socket
import mimetypes
from pathlib import Path
from flask import Flask, render_template, request, send_file, abort

app = Flask(__name__)

# Configure the root directory that users can browse
# Change this to the directory you want to expose
# ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

ROOT_DIR = '/mnt/core/work/current/rztest'
if 'MB' in socket.gethostname():
    ROOT_DIR = '/Users/robzimmelman/Documents/VSCode'

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
                * {{ box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    margin: 0;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 16px;
                    padding: 40px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    backdrop-filter: blur(10px);
                }}
                h2 {{
                    margin: 0 0 24px 0;
                    color: #1a1a2e;
                    font-weight: 600;
                    font-size: 1.5rem;
                }}
                .path {{
                    background: #1a1a2e;
                    padding: 20px;
                    border-radius: 12px;
                    word-break: break-all;
                    margin-bottom: 24px;
                    font-family: 'SF Mono', 'Fira Code', monospace;
                    font-size: 0.9rem;
                    color: #a5f3fc;
                    border: 1px solid #374151;
                }}
                .back-btn {{
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    padding: 12px 24px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 500;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                }}
                .back-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>📄 File Path</h2>
                <div class="path">{abs_path}</div>
                <a href="/browse?path={parent_dir}" class="back-btn">← Back to {parent_dir}</a>
            </div>
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
