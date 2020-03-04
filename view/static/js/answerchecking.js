angular.module('answerCheckingModule', ['ngRoute', 'generalModule', 'requestsModule'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('//')
        $interpolateProvider.endSymbol('//')
    })
   .controller('answerCheckingController', function (httpRequestsService, generalService, $filter){
        var vm = this;
        var modal = document.getElementById("myModal");
        vm.pageSize = 100;

       vm.numberOfPages=function(){
           return Math.ceil(vm.filteredanswers.length/vm.pageSize);
       }

        httpRequestsService.getAnswers()
        .then(function(response){
            vm.answers = response.data
       });

         httpRequestsService.getQuestions()
        .then(function (response) {
            vm.questions = response.data
            vm.questions = $filter('orderBy')(vm.questions, 'questionnumber', false)
        });

         httpRequestsService.getTeams()
        .then(function (response) {
            vm.teams = response.data
            vm.teams = $filter('orderBy')(vm.teams, 'teamname', false)
        });

         httpRequestsService.getPersons()
        .then(function (response) {
            vm.persons = response.data
            vm.persons = $filter('orderBy')(vm.persons, 'personname', false)
        });

        httpRequestsService.getCategories()
        .then(function (response) {
            vm.categories = response.data
            vm.categories = $filter('orderBy')(vm.categories, 'name', false)
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
                vm.answers = response.data;
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
       vm.updateAnswers  = function (){
           httpRequestsService.getAnswers(vm.filteredTeam, vm.filteredCategory, vm.filteredQuestion, vm.filteredCorrect, vm.filteredCheckedby, vm.confidenceFrom, vm.confidenceTo)
               .then(function(response){
                   vm.answers = response.data;
               });
       }

    })
