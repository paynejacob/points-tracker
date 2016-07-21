def add_allocated_points():
    pass

def calculate_price():
    pass

def play_audio():

        audio_id = 1

        a = Audio.query.filter_by(id=audio_id).one()
        #define stream chunk
        chunk = 1024

        #open a wav format music
        f = wave.open(os.path.join(current_app.config['UPLOAD_FOLDER'], a.filename),"rb")
        #instantiate PyAudio
        p = pyaudio.PyAudio()
        #open stream
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),
                        rate = f.getframerate(),
                        output = True)
        #read data
        data = f.readframes(chunk)

        #paly stream
        while data != '':
            stream.write(data)
            data = f.readframes(chunk)

        #stop stream
        stream.stop_stream()
        stream.close()

        #close PyAudio
        p.terminate()
