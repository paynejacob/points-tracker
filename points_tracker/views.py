# -*- coding: utf-8 -*-
"""Main UI section."""
import wave
import contextlib
from . import utils
import os, json, md5
from soco import SoCo
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from pydub import AudioSegment
from mutagen.apev2 import APEv2
from models import Audio, AudioTag
from werkzeug import secure_filename
from points_tracker.auth import role_required
from flask.ext.login import login_required, current_user
from flask import Blueprint, Response, render_template, flash, url_for, redirect, request, current_app, send_file

blueprint = Blueprint('main', __name__, static_folder="../static")

###
### The UI application is driven by AngularJS, so a single server-driven
### template and a few helpers are all that is needed, in addition to the API.
###

@blueprint.route("/", methods=["GET"])
@login_required
def dashboard():
    context = {}
    return render_template("points-tracker.html", **context)

@blueprint.route('/get_audio_file/<audio_id>', methods=['GET'])
def get_audio_file(audio_id):

    audio_id = audio_id.replace('.wav', '')

    return send_file(
     current_app.config['UPLOAD_FOLDER']+'/'+audio_id,
     mimetype="audio/wav",
     attachment_filename=audio_id+".wav")

@blueprint.route('/play/<audio_id>', methods=['POST'])
@login_required
def playfile(audio_id):

    a = Audio.query.filter_by(id=audio_id).one()

    if(current_app.config['PLAY_ON_SONOS']):
        sonos = SoCo(current_app.config['SONOS_IP'])

        #get sonos current state before making changes
        volume = sonos.volume

        track = sonos.get_current_track_info()
        sonos.volume = current_app.config['SONOS_VOLUME']
        sonos.play_uri(current_app.config['APP_URL']+'/get_audio_file/'+a.filename+'.wav')

        return 'done'

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
    return 'done'


@blueprint.route('/files/', defaults={'search_query': None}, methods=['GET'])
@blueprint.route('/files/<search_query>', methods=['GET'])
@login_required
def files(search_query):

    if search_query == None:
        audio = Audio.query.all()
    else:
        if "," in search_query:
            tags = AudioTag.query.filter(AudioTag.tag.in_([term.strip().upper() for term in search_query.split(',')])).all()
        else:
            tags = AudioTag.query.filter(AudioTag.tag.like("%{}%".format(search_query.upper()))).all()
        audio_ids = [tag.audio_id for tag in tags]

        priority = {}
        for tag in tags:
            priority[tag.audio_id] = priority.setdefault(tag.audio_id, 0) + 1

        prioritized_ids = sorted(priority.items(), key=lambda x: x[1], reverse=True)
        audio = Audio.query.filter(Audio.id.in_([pid[0] for pid in prioritized_ids])).all()

    return Response(response=json.dumps([a.to_json() for a in audio]))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@blueprint.route("/files/", methods=["POST"])
@login_required
def upload_file():
    if request.method == 'POST':
        if request.files:
            file = request.files['file']

            if allowed_file(file.filename):

                #save file to disk
                filename, extension = os.path.splitext(file.filename)
                filenamehash = md5.new(secure_filename(filename)).hexdigest()
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filenamehash)

                with open(filepath, 'w') as disk_file:
                    pass
                file.save(filepath)

                audiofile = AudioSegment.from_file(filepath, extension[1:])                         #load the file
                audiofile = audiofile[:current_app.config['MAX_AUDIO_DURATION_MS']]                 #trim the file
                audiofile = audiofile + -(audiofile.dBFS - current_app.config['AUDIO_DB_LEVEL'])    #level the file
                audiofile.export(filepath, "wav")                                                   #save our changes to disk

                #create the db record of the file
                audio = Audio.create(
                        name= request.form['audioName'],
                        filename= filenamehash,
                        length= audiofile.duration_seconds)

                # add the tags
                tags = [AudioTag.create(tag=tag, audio_id=audio.id) for tag in (request.form['audioName']+','+request.form['audioTags']).upper().split(',')]

    return Response(response=json.dumps({}))
