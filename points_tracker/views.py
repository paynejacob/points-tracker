# -*- coding: utf-8 -*-
"""Main UI section."""
import os, json, md5
from flask import Blueprint, Response, render_template, flash, url_for, redirect, request, current_app
from flask.ext.login import login_required, current_user
from werkzeug import secure_filename

from . import utils

from points_tracker.auth import role_required
from models import Audio, AudioTag

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

    audio = pyglet.media.StaticSource(pyglet.media.load('static/audio/'+a.filename))
    audio.play()
    return 'done'


@blueprint.route('/files/', defaults={'search_query': None}, methods=['GET'])
@blueprint.route('/files/<search_query>', methods=['GET'])
@login_required
def files(search_query):

    if search_query == None:
        audio = Audio.query.limit(10)
    else:
        tags = AudioTag.query.filter(AudioTag.tag.in_([term.upper() for term in search_query.split(' ')])).all()

        priority = {}
        for aid in tags:
            if aid in priority:
                priority[aid] +=1
            else:
                priority[aid] =1

        priority = {}
        for aid in tags:
            if aid in priority:
                priority[aid] = priority.setdefault(aid, 0) + 1

        prioritized_ids = sorted(priority.items(), key=lambda id: id[0])

        audio = Audio.query.filter(Audio.id.in_([pid[0].audio for pid in prioritized_ids])).all()

    files = [{
            'id': a.id,
            'name': a.name,
            'length': a.length
        } for a in audio]

    return Response(response=json.dumps(files))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@blueprint.route("/files/", methods=["POST"])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename, extension = os.path.splitext(file.filename)
            filenamehash = md5.new(secure_filename(filename)).hexdigest()
            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filenamehash+extension), 'w') as disk_file:
                pass
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filenamehash+extension))
        else:
            Audio.create(
                filename=filenamehash+extension,
                length=15)
    return Response(response=json.dumps({}))
