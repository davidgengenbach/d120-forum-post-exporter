(function(angular) {
    'use strict';

    angular
        .module('App', [])
        .constant('THREADS_JSON', 'data/posts.json')
        .config(function($sceProvider) {
          $sceProvider.enabled(false);
        })
        .controller('MainCtrl', function($scope, $http, THREADS_JSON) {
            getThreads()
                .then(function(threads) {
                    $scope.threads = threads;
                });

            function getThreads() {
                return $http
                    .get(THREADS_JSON)
                    .then(function(res) {
                        return res.data.threads;
                    });
            }
        });
})(angular);
