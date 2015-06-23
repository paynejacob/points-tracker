(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('AudioListCtrl', AudioListCtrl)

  AudioListCtrl.$inject = ['$scope', 'toaster', '$log', '$http', '$timeout', '$modal', 'Upload'];

  function AudioListCtrl($scope, toaster, $log, $http, $timeout, $modal, Upload) {
    var self = this;

    self.searchQuery='';
    self.playing=0;
    self.uploadProgress = 0;
    self.audio = []

    self.playAudio = function(id, length){
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
      $log.log('called');
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


    self.openAudioUploadModal = function(){
      $modal.open({
        templateUrl: '/static/partials/widgets/upload-audio-modal.html',
        size: 'lg',
        controller: 'UploadAudioCtrl',
        controllerAs: 'ctrl'
      });
    };

  }

})();

