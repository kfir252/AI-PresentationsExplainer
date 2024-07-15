#imports
import os
import uuid
import datetime
import sys

from db.dbConnection import Upload, addUpload, getUpload
from db.dbConnection import User, addUser, getUser, getUserUploads, deleteUser

#flask setup
from flask import Flask, request, jsonify, send_from_directory
app = Flask(__name__)

# data folders
UPLOAD_FOLDER = 'Server/db/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


OUTPUT_FOLDER = 'Server/db/outputs'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


#quick functions
get_timestamp = lambda: datetime.datetime.now().strftime('%Y%m%d%H%M%S')
get_new_uid = lambda: str(uuid.uuid4())


# ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ ███████╗
# ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝
# ██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║███████╗
# ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║╚════██║
# ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝███████║
#  ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝
@app.route('/upload', methods=['POST'])
def load_file_from_request():

    #check if input file is valid
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    uid = get_new_uid()

    if 'email' in request.files:
        email = request.files['email'].read().decode('utf-8')
        if not email.isspace():
            addUpload(file.filename, uid, email)
    else:
        addUpload(file.filename, uid)

    filename = f"{get_timestamp()}_{uid}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    file.save(filepath)
    return jsonify({'uid': uid})



# ███████╗████████╗ █████╗ ████████╗██╗   ██╗███████╗
# ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║   ██║██╔════╝
# ███████╗   ██║   ███████║   ██║   ██║   ██║███████╗
# ╚════██║   ██║   ██╔══██║   ██║   ██║   ██║╚════██║
# ███████║   ██║   ██║  ██║   ██║   ╚██████╔╝███████║
# ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝
@app.route('/status/<uid>', methods=['GET'])
def check_status(uid):
    upload_files = os.listdir(UPLOAD_FOLDER)
    output_files = os.listdir(OUTPUT_FOLDER)
    
    for filename in upload_files:
        if uid == filename.split('_')[1]:
            timestamp, _, original_filename = filename.split('_', 2)
            if any(uid in fname for fname in output_files):
                output_filepath = next(fname for fname in output_files if uid in fname)
                with open(os.path.join(OUTPUT_FOLDER, output_filepath), 'r') as f:
                    explanation = f.read()
                return jsonify({
                    'status': 'done',
                    'filename': original_filename,
                    'timestamp': timestamp,
                    'explanation': explanation
                })
            else:
                return jsonify({
                    'status': 'pending',
                    'filename': original_filename,
                    'timestamp': timestamp,
                    'explanation': None
                })
                
    return jsonify({'status': 'unknown_uid',
                    'filename': None,
                    'timestamp': None,
                    'explanation': None}), 404





#C:/Users/kfirl/Desktop/presentation.pptx


if __name__ == '__main__':
    app.run()
