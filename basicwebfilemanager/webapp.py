import os
from flask import Flask, render_template, send_file, abort

app = Flask(__name__)

# Base directory to browse (change this to the directory you want to make accessible)
BASE_DIR = '/'

@app.route('/')
def list_files():
    try:
        # Normalize and validate the base directory
        base_path = os.path.abspath(BASE_DIR)
        
        # List to store file and directory information
        file_list = []
        
        # Walk through the directory
        for root, dirs, files in os.walk(base_path):
            # Get the relative path from the base directory
            relative_path = os.path.relpath(root, base_path)
            
            # Add directories
            for dir_name in dirs:
                full_dir_path = os.path.join(root, dir_name)
                rel_dir_path = os.path.join(relative_path, dir_name)
                file_list.append({
                    'name': dir_name,
                    'path': rel_dir_path,
                    'type': 'directory',
                    'full_path': full_dir_path
                })
            
            # Add files
            for file_name in files:
                full_file_path = os.path.join(root, file_name)
                rel_file_path = os.path.join(relative_path, file_name)
                try:
                    file_size = os.path.getsize(full_file_path)
                except Exception:
                    file_size = 0
                
                file_list.append({
                    'name': file_name,
                    'path': rel_file_path,
                    'type': 'file',
                    'full_path': full_file_path,
                    'size': file_size
                })
        
        return render_template('file_browser.html', files=file_list, base_dir=base_path)
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/download/<path:filepath>')
def download_file(filepath):
    try:
        # Construct the full path and normalize it
        full_path = os.path.abspath(os.path.join(BASE_DIR, filepath))
        
        # Ensure the file is within the base directory
        if not full_path.startswith(os.path.abspath(BASE_DIR)):
            abort(403)  # Forbidden
        
        # Check if file exists
        if not os.path.exists(full_path):
            abort(404)
        
        # Send the file for download
        return send_file(full_path, as_attachment=True)
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)