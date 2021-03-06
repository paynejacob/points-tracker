# -*- coding: utf-8 -*-
"""Admin module. Tees up the Flask-SuperAdmin blueprint.
"""
from flask import render_template
from flask.ext.login import current_user
from flask.ext.superadmin import AdminIndexView, Admin as SuperAdmin
from flask.ext.superadmin.model import ModelAdmin

from points_tracker.auth import role_required
from points_tracker.extensions import db



class ProtectedModelView(ModelAdmin):

    session = db.session

    def is_accessible(self):
        return role_required('admin').has_role()


class ProtectedAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return role_required('admin').has_role()


class Admin(object):

    def init_app(self, app):
        from points_tracker.auth import models as auth_models
        from points_tracker import models as ui_models
        index_view = ProtectedAdminIndexView(name='Admin Console')
        admin = SuperAdmin(app, 'points_tracker', index_view=index_view)
        admin.register(auth_models.User, ProtectedModelView)
        admin.register(auth_models.Role, ProtectedModelView)
        admin.register(ui_models.Audio, ProtectedModelView)
        admin.register(ui_models.AudioTag, ProtectedModelView)
