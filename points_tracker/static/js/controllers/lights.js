(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('LightsCtrl', LightsCtrl)

  LightsCtrl.$inject = ['hue', '$scope'];

  function LightsCtrl(hue, $scope) {
    var self = this;
    //auth data for hue lights
    var myHue = hue;
    myHue.setup({
      username: window.HUE.username,
      bridgeIP: window.HUE.bridgeIP,
      debug: true
    });

    myHue.getLights().then(function(lights) {
      $scope.lights = lights;
    });
    return myHue.getLights().then(function(lights) {
      var changeBrightness, lazyChangeBrightness;
      $scope.lights = lights;
      $scope.setLightStateOn = function(light, state) {
        return myHue.setLightState(light, {
          on: state
        }).then(function() {
          return $scope.lights[light].state.on = state;
        });
      };
      $scope.triggerAlert = function(light, alert) {
        return myHue.setAlert(light, alert);
      };
      $scope.setEffect = function(light, effect) {
        return myHue.setEffect(light, effect).then(function() {
          return $scope.lights[light].state.effect = effect;
        });
      };
      changeBrightness = function(light, value) {
        return myHue.setLightState(light, {
          "bri": value
        });
      };
      lazyChangeBrightness = _.debounce(changeBrightness, 600);
      $scope.changeBrightness = function(light, value) {
        return lazyChangeBrightness(light, value);
      };
      myHue.getGroups().then(function(groups) {
        $scope.groups = groups;
        $scope.deleteGroup = function(group) {
          return myHue.deleteGroup(group).then(function() {
            return delete $scope.groups[group];
          });
        };
        return $scope.setGroupStateOn = function(group, state) {
          return myHue.setGroupState(group, {
            on: state
          }).then(function() {
            $scope.groups[group].action.on = state;
            return angular.forEach($scope.groups[group].lights, function(value) {
              return $scope.lights[value].state.on = state;
            });
          });
        };
      });
    });
  };

})();
