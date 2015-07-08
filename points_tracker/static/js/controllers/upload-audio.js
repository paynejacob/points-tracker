(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('AudioUploadCtrl', AudioUploadCtrl)

  AudioUploadCtrl.$inject = ['$scope', 'toaster', '$log', 'FileUploader', '$http'];

  function AudioUploadCtrl($scope, toaster, $log, FileUploader, $http) {
    var self = this;

    $scope.master = {tags:"", name:""};
    $scope.audio = angular.copy($scope.master);
    $scope.uploader = $scope.uploader = new FileUploader({
            url: '/files/'
        });
    $scope.uploading = false;

    $scope.submit = function(audio) {
      if($scope.audioUploadForm.$valid){
        if($scope.uploader.queue.length === 0){
          toaster.pop('error', "Audio File", "The audio file is required");
          return
        }
        $scope.uploading = true;
        $scope.uploader.uploadAll();
        $scope.uploader.onCompleteAll = function() {
            $http({
              url: '/files/',
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              data: JSON.stringify({
                audioName: audio.name,
                audioTags: audio.tags,
                audioFileName: '410dac82c3bc360ac8737268555953d5.mp3'
            })})
        };
      }
      $scope.master = angular.copy(audio);
    };
  }
})();
