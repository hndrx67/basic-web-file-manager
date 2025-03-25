from flask import Flask, render_template, send_from_directory, request, abort
import os

app = Flask(__name__)

BASE_DIR = "/"  # Root directory of the Ubuntu server

@app.route("/")
@app.route("/browse", defaults={"path": ""})
@app.route("/browse/<path:path>")
def browse(path):
    abs_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(abs_path):
        abort(404)

    items = os.listdir(abs_path)
    files = []
    directories = []

    for item in items:
        item_path = os.path.join(abs_path, item)
        if os.path.isfile(item_path):
            files.append(item)
        else:
            directories.append(item)

    return render_template("index.html", path=path, files=files, directories=directories)

@app.route("/download/<path:path>")
def download(path):
    abs_path = os.path.join(BASE_DIR, path)
    
    if not os.path.isfile(abs_path):
        abort(404)

    directory = os.path.dirname(abs_path)
    filename = os.path.basename(abs_path)

    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
