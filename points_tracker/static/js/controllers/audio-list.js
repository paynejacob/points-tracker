(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('AudioListCtrl', AudioListCtrl)

  AudioListCtrl.$inject = ['$scope', 'toaster', '$log', '$http', '$timeout'];

  function AudioListCtrl($scope, toaster, $log, $http, $timeout) {
    var self = this;

    self.searchQuery='';
    self.playing=0;
    self.uploadProgress = 0;
    self.audio = []

    self.playAudio = function(id, length){
      console.log('called');
      $http.post(
        '/play/'+id,
        {}
      )
      .error(function(error){
        $log.error('audio failed to play: '+error);
        self.playing='error';
      })
      .success(function(audio){
        $log.log('played');
        self.playing=id;
        $log.log(length);
        $timeout(function(){self.playing=0;}, length*1000+500);
      });
    };

    self.getAudioList = function(){
      $http.get(
        '/files/'+self.searchQuery,
        {}
      )
      .error(function(error){
        $log.error('Fetch audio list failed: '+error);
      })
      .success(function(audio){
        self.audio = audio;
      });
    };
    angular.element(document).ready(function () {
        self.getAudioList();
    });
  }
})();
