(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .filter('formatAudioLength', formatAudioLength)

  formatAudioLength = function(){
    return function(input){
      var mins = Math.floor(input/60);
      var sec = input-mins*60;
      sec = (sec<10) ? '0'+sec : sec
      mins = (mins<10) ? '0'+mins : mins
      return mins+':'+sec;
    };
  };
  
})();
