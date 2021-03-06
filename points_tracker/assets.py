# -*- coding: utf-8 -*-
""" Define our asset bundles for front-end minification """

import json, os
from points_tracker.utils import angular_filter
from flask_assets import Bundle, Environment

vendor_css = Bundle(
    "libs/bootswatch-dist/css/bootstrap.min.css",
    "libs/angularjs-toaster/toaster.min.css",
    filters="cssmin",
    output="vendor.min.css"
)

app_css = Bundle(
    "css/style.scss",
    filters=["pyscss", "cssmin"],
    output="app.min.css"
)

vendor_js = Bundle(
    "libs/jquery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.min.js",
    "libs/angular/angular.min.js",
    "libs/angular-bootstrap/ui-bootstrap-tpls.min.js",
    "libs/angular-ui-router/release/angular-ui-router.min.js",
    "libs/angular-resource/angular-resource.min.js",
    "libs/angular-animate/angular-animate.min.js",
    "libs/lodash/lodash.min.js",
    "libs/moment/min/moment.min.js",
    "libs/angularjs-toaster/toaster.min.js",
    "libs/angular-file-upload/angular-file-upload.min.js",
    filters='jsmin',
    output="vendor.min.js"
)

app_js = Bundle(
    "js/modules.js", # modules.js must be first!
    "js/points_tracker.js",
    "js/services.js",
    "js/controllers/*.js",
    "js/filters.js",
    "js/vendor/*.js",
    filters="jsmin",
    output="app.min.js"
)

angular_templates_js = Bundle(
    "partials/*.html",
    "partials/widgets/*.html",
    filters='angulartemplatecache',
    output="partials.min.js"
)

assets = Environment()

assets.register("app_js", app_js)
assets.register("vendor_js", vendor_js)
assets.register("angular_templates_js", angular_templates_js)
assets.register("app_css", app_css)
assets.register("vendor_css", vendor_css)
