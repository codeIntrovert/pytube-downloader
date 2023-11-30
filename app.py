from time import time
from pytube import YouTube
from threading import Thread
from cleaner import clear_directory
from flask import Flask, render_template, request, send_file

# App instance
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Automatically clean the /temp
cleaner_thread = Thread(target=clear_directory)

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Download endpoint
@app.route('/streams', methods=['POST'])
def streams():
    # Media link
    link = request.form['text']
    
    # Download type:
    type = request.form['type']

    # Instance pytube
    pytube = YouTube(link)

    # Get streams
    is_audio = type == 'audio'
    if(is_audio):
        streams = pytube.streams.filter(type=type, progressive="False").order_by("abr").desc()
    else:
        streams = pytube.streams.filter(type=type, progressive="False").order_by("resolution").desc()

    return render_template('streams.html', link=link, streams=streams, is_audio=is_audio)
    
@app.route('/download', methods=['POST'])
def download(link : str, audio: bool):
    # Instance pytube
    pytube = YouTube(link)

    # Get the stream
    stream = pytube.streams.get_audio_only() if audio else pytube.streams.get_highest_resolution()

    # Generate filename
    filename = f'temp{round(time() * 1000)}.{"mp3" if audio else "mp4"}'

    # Download
    try:
        stream.download(output_path='temp', filename=filename)
        # Download the file (browser)
        return send_file( f'temp/{filename}', as_attachment=True)
    except:
        # Render index again (with error)
        return render_template('index.html', error='Invalid link')   

# Scope verification
if __name__ == "__main__":
    # Start the cleaner
    cleaner_thread.start()

    # Start the app
    app.run(debug=True) # TODO: TURN OFF DEBUG MODE

    # Join cleaner before end
    cleaner_thread.join()