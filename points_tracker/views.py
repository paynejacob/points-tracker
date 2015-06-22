# -*- coding: utf-8 -*-
"""Main UI section."""
from flask import Blueprint, Response, render_template, flash, url_for, redirect, request, current_app
from flask.ext.login import login_required, current_user

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
def playfile(audio_id):
    a = Audio.query.filter_by(id=audio_id).one()

    audio = pyglet.media.StaticSource(pyglet.media.load('audio_files/'+a.filename))
    audio.play()
    return 'done'


@blueprint.route('/files/', defaults={'search_query': None}, methods=['POST'])
@blueprint.route('/files/<search_query>', methods=['POST'])
def files(search_query):

    if search_query:
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
