(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('AudiListCtrl', AudiListCtrl)

  AudiListCtrl.$inject = ['$scope', 'toaster', '$log', '$http', '$timeout'];

  function AudiListCtrl($scope, toaster, $log, $http, $timeout) {
    var self = this;

    self.searchQuery='';
    self.playing=0;

    self.playAudio = function(id, length){
      $http.post(
        '/play/'+id,
        {}
      )
      .error(function(error){
        console.error('audio failed to play: '+error);
        self.playing='error';
      })
      .success(function(audio){
        console.log('played');
        self.playing=id;
        console.log(length);
        $timeout(function(){self.playing=0;}, length*1000+500);
      });
    };

    self.getAudioList = function(){
      console.log('called');
      $http.post(
        '/files/'+self.searchQuery,
        {}
      )
      .error(function(error){
        console.error('Fetch audio list failed: '+error);
      })
      .success(function(audio){
        self.audio = audio;
      });
    };
  }

})();

