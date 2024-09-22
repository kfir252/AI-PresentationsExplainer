#imports
import os
import uuid
import datetime
import sys

from db.dbConnection import Upload, addUpload, getUpload, GetUploadByEmailAndFilename
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

#done!
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
        print(email)
        addUpload(file.filename, uid, email)
    else:
        print('no email given')
        addUpload(file.filename, uid)
        
    filename = uid
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    file.save(filepath)
    return jsonify({'uid': uid})



# ███████╗████████╗ █████╗ ████████╗██╗   ██╗███████╗
# ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║   ██║██╔════╝
# ███████╗   ██║   ███████║   ██║   ██║   ██║███████╗
# ╚════██║   ██║   ██╔══██║   ██║   ██║   ██║╚════██║
# ███████║   ██║   ██║  ██║   ██║   ╚██████╔╝███████║
# ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝

def getUploadData(upload):
    if upload == None:
        return jsonify({'status': 'unknown_uid',
                'filename': None,
                'timestamp': None,
                'explanation': None}), 404
    elif upload.status == 'done':
        with open(os.path.join(OUTPUT_FOLDER, str(upload.uid)+'.json'), 'r') as f:
            explanation = f.read()
            return jsonify({
                'status': upload.status,
                'filename': upload.filename,
                'timestamp': upload.upload_time,
                'explanation': explanation
        })
    else:
        return jsonify({
                'status': upload.status,
                'filename': upload.filename,
                'timestamp': upload.upload_time,
                'explanation': None
        })


@app.route('/status/<uid>', methods=['GET'])
def check_file_status(uid):
    return getUploadData(getUpload(uid))


@app.route('/file_by_mail/<info>', methods=['GET'])
def check_file_status_by_mail(info):
    email, filename = tuple(info.split('::'))
    return getUploadData(GetUploadByEmailAndFilename(email, filename))


#C:/Users/kfirl/Desktop/presentation.pptx


if __name__ == '__main__':
    app.run()
