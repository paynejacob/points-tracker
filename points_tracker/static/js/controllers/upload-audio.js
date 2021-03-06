(function() {
  'use strict';

  angular
    .module('points_tracker.controllers')
    .controller('AudioUploadCtrl', AudioUploadCtrl)

  AudioUploadCtrl.$inject = ['toaster', '$log', 'FileUploader', '$http', '$state'];

  function AudioUploadCtrl(toaster, $log, FileUploader, $http, $state) {
    var self = this;

    self.master = {tags:"", name:""};
    self.audio = angular.copy(self.master);
    self.uploader = self.uploader = new FileUploader({
            url: '/files/'
        });
    self.uploading = false;

    self.submit = function(audio) {
      if(self.audioUploadForm.$valid){
        if(self.uploader.queue.length === 0){
          toaster.pop('error', "Audio File", "The audio file is required");
          return
        }
        self.uploading = true;
        
        self.uploader.onBeforeUploadItem = function(item) {
            //append form data to request
            item.formData.push({
              audioName: self.audio.name,
              audioTags: self.audio.tags
            })
            $log.info('onBeforeUploadItem', item);
        };
        
        self.uploader.uploadAll();
        
        self.uploader.onCompleteAll = function() {
          if(self.error) return;
          $state.go('audio-list');
          $log.info("audio file uploaded",value);
          toaster.pop('success', "Your file has been added");
        };

        self.uploader.onErrorItem = function(item, response, status, headers){

          $log.error("Error: item failed to upload", item);
          toaster.pop('error', 'Your file failed to upload');
          self.error = true;
          self.uploading = false;
        };

        self.uploader.onCancelItem = function(item, response, status, headers) {
          self.uploading = false;
        };
      }
      self.master = angular.copy(audio);
    };
  }
})();
