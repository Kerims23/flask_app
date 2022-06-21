from flask import Flask, render_template, redirect, request, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
import os

#in terminal install 
#pip install flask 
#pip install flask_wtf wtforms


#this creates flask app
app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
#this is the content max size
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 # 64MB
#this enables what files can be uploaded
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif','.pdf','.docx']



@app.route('/')
def index():
  files = os.listdir(app.config['UPLOAD_DIRECTORY'])
  images = []
#reads through the files and runs through 1 file at a time
  for file in files:
    if os.path.splitext(file)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
      images.append(file)
  
  return render_template('index.html', images=images)



@app.route('/upload', methods=['POST'])
def upload():
  try:
    file = request.files['file']
    if file:
      extension = os.path.splitext(file.filename)[1].lower()
      #if it doesn't pass extension then it will say declined 
      if extension not in app.config['ALLOWED_EXTENSIONS']:
        return 'File is not an recognizable.'
      file.save(os.path.join(
        app.config['UPLOAD_DIRECTORY'],
        secure_filename(file.filename)
      ))
  #this is a import that says the files are too big
  except RequestEntityTooLarge:
    return 'File is larger than the 64MB limit.'
  
  return redirect('/')



@app.route('/serve-image/<filename>', methods=['GET'])
def serve_image(filename):
  return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)

