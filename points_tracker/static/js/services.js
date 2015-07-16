(function(){
  'use strict'

  angular
    .module('points_tracker.services')
    .factory('Audio', Audio);

  Audio.$inject = ['$resource'];

  function Audio($resource){
    return $resource('/files/:query', {limit: 10000}, {
      query: {method:'GET', isArray: true},
      play: {method:'POST', url:'/play/:id', params:{'id': '@id'}},
    });
  }

})();