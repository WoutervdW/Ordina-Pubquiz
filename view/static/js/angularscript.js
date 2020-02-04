angular.module('module', ['ngRoute'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('//')
        $interpolateProvider.endSymbol('//')
    })
    .controller('controller', function ($scope, $http, $location, $window, $filter) {
        $scope.removeOtherStuff = function () {
            $http.post("/api/v1.0/nuke/all")
            window.location.reload()
        }

        $scope.showloadingsheetsbar = function () {
            $scope.loadingsheets = true;
        }

        $scope.fileChanged = function(files) {
             document.getElementById("custom-file-label").innerHTML = files[0].name;
        }
    })




