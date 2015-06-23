(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('UploadAudioCtrl', UploadAudioCtrl)

  UploadAudioCtrl.$inject = ['$scope', 'toaster', '$log', 'Upload'];

  function UploadAudioCtrl($scope, toaster, $log, Upload) {
    var self = this;

    self.uploadProgress = 0;

    self.uploadAudio = function(files, event) {
      if (files && files.length > 0) {
        _.each(files, function(file) {
          Upload.upload({
            url: '/files/',
            fields: {type: 'audio'},
            file: file
          }).then(
            function(data, status, headers, config) {
              $scope.close();
              toaster.pop("success", "Your upload was received successfully.");
            }, function(reply, status, headers){
              $scope.close();
              $log.error("error uploading audio", reply, status, headers);
            }, function(evt) {
              // Only let it go to 99 until we're done refreshing report at end...
              self.uploadProgress = Math.min(parseInt(100.0 * evt.loaded / evt.total), 99);
            });
        });
      }
    };

  }

})();

