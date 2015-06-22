(function() {
  'use strict';

  // Third party shims
  angular.module('underscore', []).factory('_', function() { return window._; });
  angular.module('moment', []).factory('moment', function() { return window.moment; });
  angular.module('components', ['underscore', 'moment']); //see vendor/dateTransformer.js

  // Define modules here so that file concatenation ordering doesn't
  // break the app.  This is a poor man's Browserify/RequireJS.
  angular.module('points_tracker.services', [
    'ngResource'
  ]);
  angular.module('points_tracker.controllers', []);
  angular.module('points_tracker.filters', []);
  angular.module('points_tracker', [
    'components',
    'ui.bootstrap',
    'ui.router',
    'flask-assets-templates',
    'points_tracker.services',
    'points_tracker.controllers',
    'points_tracker.filters',
    'toaster'
  ]);

})();
