(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('LightsCtrl', LightsCtrl)

  LightsCtrl.$inject = ['hue'];

  function LightsCtrl(hue) {
    var self = this;

    //auth data for hue lights
    var myHue = hue;
    myHue.setup({
      username: "myuser",
      bridgeIP: "yourbridge",
      debug: true
    });
  }
})();
