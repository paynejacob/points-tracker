(function() {
  'use strict';

  angular
    .module('points_tracker')
    .config(PointsConfig)
    .run(PointsRun);

  PointsConfig.$inject = ['$stateProvider', '$urlRouterProvider', '$resourceProvider'];

  function PointsConfig($stateProvider, $urlRouterProvider, $resourceProvider) {
    $urlRouterProvider.otherwise("/");

    // Normal analyst states
    $stateProvider
      .state('dashboard', {
        url: '/',
        templateUrl: '/static/partials/dashboard.html',
      })
      .state('audio-list', {
        url: '/audio-list',
        templateUrl: '/static/partials/audio-list.html',
      });

    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;

  }

  PointsRun.$inject = ['$rootScope'];

  function PointsRun($rootScope) {
    // Expose `_.` methods in any template
    $rootScope._ = _;

    $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
      // Scroll to top of page on any state change.
      // This is coupled with the `autoscroll="false"` on the ui-view tag
      // in points_tracker/templates/dashboard.html
      $('html, body').animate({scrollTop: 0}, 200);

    });
  }
})();
