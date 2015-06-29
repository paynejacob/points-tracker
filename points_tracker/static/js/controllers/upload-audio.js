(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('AudioUploadCtrl', AudioUploadCtrl)

  AudioUploadCtrl.$inject = ['$scope', 'toaster', '$log', 'Upload'];

  function AudioUploadCtrl($scope, toaster, $log, Upload) {
    var self = this;

    self.uploadProgress = 0;
    self.filename='';
    self.tags ='';
    self.audiofile=false;

    self.uploadAudio = function(file, event) {
      if (file[0]) {
        Upload.upload({
          url: '/files/',
          fields: {type: 'audio'},
          file: file[0]
        }).then(
          function(data, status, headers, config) {
            toaster.pop("success", "Your upload was received successfully.");
          }, function(reply, status, headers){
            $log.error("error uploading audio", reply, status, headers);
          }, function(evt) {
            self.uploadProgress = Math.min(parseInt(100.0 * evt.loaded / evt.total), 100);
            self.filename = file[0].name
          });
      }
    };

    self.setAudioInfo = function(){
      
    }
  }
})();
