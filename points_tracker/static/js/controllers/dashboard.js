(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('DashboardCtrl', DashboardCtrl)

  DashboardCtrl.$inject = ['$scope', 'toaster', '$log'];

  function DashboardCtrl($scope, toaster, $log) {
    var self = this;

    self.title = "Welcome!"

  }

})();
