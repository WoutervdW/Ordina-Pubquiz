angular.module('uploadModule', ['ngRoute'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('//')
        $interpolateProvider.endSymbol('//')
    })

    .controller('uploadController', function (){
        vm = this;
        vm.showloadingsheetsbar = function () {
            vm.loadingsheets = true;
        }

        vm.fileChanged = function(files) {
            document.getElementById("custom-file-label").innerHTML = files[0].name;
        }
    })