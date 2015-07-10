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
        $scope.uploader.onBeforeUploadItem = function(item) {
            //append form data to request
            item.formData.push({
              audioName: audio.name,
              audioTags: audio.tags
            })
            console.info('onBeforeUploadItem', item);
        };
        $scope.uploader.uploadAll();
        $scope.uploader.onCompleteAll = function(value) {
          return
        };
      }
      $scope.master = angular.copy(audio);
    };
  }
})();
