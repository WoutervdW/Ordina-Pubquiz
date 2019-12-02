// define angular interpolationtags as {a a}
angular.module('module', [])
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
    })
     .controller('questioncontroller', function($scope, $http){
     $http({
                method: "GET",
                url: "/api/v1.0/questions"
                }).then(function mySuccess(response){
                    $scope.questions = response.data;
                });
        $scope.propertyName = 'question';
        $scope.reverse = 'false';
        $scope.sortBy = function(propertyName) {
            $scope.reverse = $scope.propertyName === propertyName ? !$scope.reverse : false;
            $scope.propertyName = propertyName;
        }

    })

    .controller('indexcontroller', function($scope, $http){
        $http({
                method: "GET",
                url: "/api/v1.0/teams"
                }).then(function mySuccess(response){
                    $scope.teams = response.data;
                });
        $scope.propertyName = 'score';
        $scope.reverse = 'false';
        $scope.sortBy = function(propertyName) {
            $scope.reverse = $scope.propertyName === propertyName ? !$scope.reverse : false;
            $scope.propertyName = propertyName;
        }
    })
