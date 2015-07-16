(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('AudioListCtrl', AudioListCtrl)

  AudioListCtrl.$inject = ['$scope', 'toaster', '$log', '$http', '$timeout', 'Audio'];

  function AudioListCtrl($scope, toaster, $log, $http, $timeout, Audio) {
    var self = this;

    self.searchQuery = '';
    self.playing = false;
    self.loading = true;
    self.uploadProgress = 0;
    self.audio = []

    self.playAudio = function(audio){
      if(self.playing) return;
      self.playing = audio;
      Audio.play(
        audio,
        function(payload){
          $timeout(function(){
            self.playing=false;
          }, audio.length*1000);
        },
        function(error){
          $log.error('audio failed to play: '+error);
          toaster.pop('error', 'Your audio failed to play');
          self.playing=false;
        });
    };

    self.getAudioList = function(){
      Audio.query({query: self.searchQuery},
        function(payload){
          self.audio = payload;
          self.loading = false;
        },
        function(error){
          $log.error('Fetch audio list failed: '+error);
          self.loading = false;
        });
    };
    self.getAudioList();

   $scope.$watch(
      function() {
        return self.searchQuery;
      },
      function(newVal, oldVal) {
        if (newVal==oldVal) { return; }
        audioQueryDebounced();
      },
      true
    );

    var audioQueryDebounced = _.debounce(function() {
      self.loading = true;
      self.getAudioList()
    }, 1000);
  }

})();
