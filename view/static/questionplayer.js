angular.module('playerModule', ['ngRoute'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('//')
        $interpolateProvider.endSymbol('//')
    })
   .controller('pubquizcontroller', function ($http, $filter, $interval) {
        var vm = this;
        $http({
            method: "GET",
            url: "/api/v1.0/questions"
        }).then(function (response) {
            vm.questions = response.data;
            vm.questions = vm.questions.filter(q => q.questionnumber > 0
        );
            vm.questions = $filter('orderBy')(vm.questions, 'questionnumber', false);
            showQuestions();
        });

        function showQuestions() {
            i = 0;
            var showQuestion = function () {
                if (i < vm.questions.length) {
                    vm.displayedquestion = vm.questions[i];
                    i = i + 1;
                } else {
                    vm.displayedquestion.questionnumber = "";
                    vm.displayedquestion.question = "einde pubquiz";
                }
            }
            showQuestion();
            $interval(showQuestion, 300);
        };
    })