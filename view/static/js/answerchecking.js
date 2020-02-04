angular.module('answerCheckingModule', ['ngRoute', 'generalModule', 'requestsModule'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('//')
        $interpolateProvider.endSymbol('//')
    })
   .controller('answerCheckingController', function ($window, httpRequestsService, generalService){
        var vm = this;
        var modal = document.getElementById("myModal");

        httpRequestsService.getAnswers()
        .then(function (response) {
            vm.answers = response.data
        });

         httpRequestsService.getQuestions()
        .then(function (response) {
            vm.questions = response.data
        });

         httpRequestsService.getTeams()
        .then(function (response) {
            vm.teams = response.data
        });

         httpRequestsService.getPersons()
        .then(function (response) {
            vm.persons = response.data
        });

        httpRequestsService.getCategories()
        .then(function (response) {
            vm.categories = response.data
        });


        vm.updateAnswerCheck = function (answer) {
            var data = {"id": answer.id, "correct": answer.correct}
            httpRequestsService.updateAnswer(JSON.stringify(data))
            .then(function (response) {
                answer.checkedby = response.data;
            })
        }

        vm.deleteAllAnswers = function () {
            r = confirm("Alle antwoorden zullen worden verwijderd. Dit kan niet ongedaan gemaakt worden.")
            if (r == true){
                httpRequestsService.deleteAllAnswers()
                vm.answers = [];
            }
        }

         vm.checkAllAnswers = function () {
            vm.checkinganswers = true;
            httpRequestsService.checkAnswers()
            .then(function (response) {
                vm.checkinganswers = false;
                window.location.reload();
            })
        }

        vm.showModal = function () {
            modal.style.display = "block";
        }

        vm.closeModal = function () {
            modal.style.display = "none";
        }

         vm.sortBy = function(propertyName){
            result = generalService.sortBy(vm.reverse, vm.propertyName, propertyName)
            vm.reverse = result[0]
            vm.propertyName = result[1]
        }
    })