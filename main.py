from flask import Flask, render_template, request, send_file, after_this_request
from downloader import ytDownload
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def download():
    link = request.form['text']
    filename = ytDownload(link)

    if(filename):
        filePath = f'temp/{filename}'
        #TODO: DELETE AFTER SEND
        return send_file(filePath, as_attachment=True)
    else:
        return render_template('index.html')

# TODO: TURN OFF DEBUG MODE
app.run(debug=True)