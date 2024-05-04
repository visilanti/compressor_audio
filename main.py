from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import io
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def upload():
    if request.method == 'GET':
        return '''
            <h1>Praktikum</h1>
            <form method="POST" action="/audio" enctype="multipart/form-data">
                <label for="file">Audio Compression : </label>
                <input type="file" id="file" name="file">
                <button type="submit">Compress</button>
            </form>
        '''
    else:
        return '''
        <h1>Uknown method</h1>
    '''

@app.route('/audio', methods=['POST'])
def audio_compression():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_name = secure_filename(file.filename)
            file_path = os.path.join('uploads', file_name)  # Assuming 'uploads' is the directory where files are uploaded
            file.save(file_path)  # Save the uploaded file to the specified directory
            audio_io = io.BytesIO()
            audio = AudioSegment.from_mp3(file_path)
            audio.export(audio_io, format='mp3', bitrate='64k')
            # # Clean up: remove the uploaded file after processing
            # os.remove(file)
            return send_file(
                audio_io,
                as_attachment=True,
                download_name=f'compressed_{file_name}',
                mimetype='audio/mp3'
            )
        else: 
            return '''
            <h1>File not Found</h1>
        '''
    else:
        return '''
        <h1>Uknown method</h1>
    '''



        

if __name__ == '__main__':
    app.run(debug=True)

