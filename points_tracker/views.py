# -*- coding: utf-8 -*-
"""Main UI section."""
import pyglet
from . import utils
import os, json, md5
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from pydub import AudioSegment
from mutagen.apev2 import APEv2
from models import Audio, AudioTag
from werkzeug import secure_filename
from points_tracker.auth import role_required
from flask.ext.login import login_required, current_user
from flask import Blueprint, Response, render_template, flash, url_for, redirect, request, current_app

#use alsa
pyglet.options['audio'] = ('alsa', 'openal', 'silent')

blueprint = Blueprint('main', __name__, static_folder="../static")

###
### The UI application is driven by AngularJS, so a single server-driven
### template and a few helpers are all that is needed, in addition to the API.
###

@blueprint.route("/", methods=["GET"])
@login_required
def dashboard():
    context = {}
    return render_template("dashboard.html", **context)


@blueprint.route('/play/<audio_id>', methods=['POST'])
@login_required
def playfile(audio_id):
    a = Audio.query.filter_by(id=audio_id).one()
    audio = pyglet.media.StaticSource(pyglet.media.load(os.path.join(current_app.config['UPLOAD_FOLDER'], a.filename)))
    audio.play()
    return 'done'


@blueprint.route('/files/', defaults={'search_query': None}, methods=['GET'])
@blueprint.route('/files/<search_query>', methods=['GET'])
@login_required
def files(search_query):

    if search_query == None:
        audio = Audio.query.limit(request.args.get('limit'))
    else:
        tags = AudioTag.query.filter(AudioTag.tag.in_([term.upper() for term in search_query.split(' ')])).all()
        audio_ids = [tag.audio for tag in tags]

        priority = {}
        for audio_id in audio_ids:
            if audio_id not in priority:
                priority[audio_id] = 0

        for tag in tags:
            priority[tag.audio] +=1

        prioritized_ids = sorted(priority.items(), key=lambda x: x[1], reverse=True)
        audio = Audio.query.filter(Audio.id.in_([pid[0] for pid in prioritized_ids[:request.args.get('limit')]])).all()

    return Response(response=json.dumps([{
            'id': a.id,
            'name': a.name,
            'length': a.length
        } for a in audio]))

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

                if extension == ".mp3":
                    length = int(round(MP3(filepath).info.length))
                    sound = AudioSegment.from_mp3(filepath)
                    sound.export(filepath, format="wav")
                elif extension == ".mp4":
                    length = int(round(MP4(filepath).info.length))
                    sound = AudioSegment.from_file(filepath)
                    sound.export(filepath, format="wav")
                elif extension == ".wav":
                    length = 0
                else:
                    length = 0

                #create the db record of the file
                audio = Audio.create(
                        name= request.form['audioName'],
                        filename= filenamehash,
                        length= length)
                # add the tags
                tags = [AudioTag.create(tag=tag, audio=audio.id) for tag in (request.form['audioName']+' '+request.form['audioTags']).upper().split()]

    return Response(response=json.dumps({}))
