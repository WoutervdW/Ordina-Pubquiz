// define angular interpolationtags as {a a}
angular.module('module', [])
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
    })
    //controller
    .controller('controller', function($scope, $http){
        $http({
            method: "GET",
            url: "/api/v1.0/teams"
        }).then(function (response){
            $scope.teams = response.data;
        });
         $http({
            method: "GET",
            url: "/api/v1.0/questions"
        }).then(function (response){
            $scope.questions = response.data;
        });
        $http({
            method: "GET",
            url: "/api/v1.0/subanswers"
        }).then(function (response){
            $scope.subanswers = response.data;
        });
        $http({
            method: "GET",
            url: "/api/v1.0/variants"
        }).then(function (response){
            $scope.variants = response.data;
        });
         $http({
            method: "GET",
            url: "/api/v1.0/categories"
        }).then(function (response){
            $scope.categories = response.data;
        });
        $http({
            method: "GET",
            url: "/api/v1.0/persons"
        }).then(function (response){
            $scope.persons = response.data;
        });
        $http({
            method: "GET",
            url: "/api/v1.0/answers"
        }).then(function (response){
            $scope.answers = response.data;
        });
        $http({
            method: "GET",
            url: "/api/v1.0/subanswersgiven"
        }).then(function (response){
            $scope.subanswersgiven = response.data;
        });

        $scope.sortBy = function sortBy(propertyName){
            $scope.reverse = $scope.propertyName === propertyName ? !$scope.reverse : false;
            $scope.propertyName = propertyName;
        }
        $scope.addQuestion = function(category_id){
            var data = {"question": $scope.newquestion, "correct_answer": $scope.newquestioncorrect_answer, "category_id": $scope.newquestioncategory, "person_id": $scope.getLoggedinPerson().id, "active":$scope.newquestionactive};
            $http.post("/api/v1.0/newquestion", JSON.stringify(data))
            $scope.questions.push(data);
            $scope.newquestion = "";
            $scope.newquestioncorrect_answer = "";
        }
        $scope.updateQuestionActive = function(question){
            var data = {"id":question.id, "active":question.active}
            $http.post("/api/v1.0/updatequestion", JSON.stringify(data))
        }
        $scope.updateAnswerCheck = function(answer){
            var data = {"id": answer.id, "correct": answer.correct, "person_id":$scope.getLoggedinPerson().id}
            $http.post("/api/v1.0/updateanswer", JSON.stringify(data))
        }
        $scope.getCategoryName = function(category_id){
            var c = $scope.categories.find(c => c.id == category_id);
            return c.name;
        }
        $scope.getPersonName = function(person_id){
            var p = $scope.persons.find(person => person.id == person_id);
            return p.personname;
        }
        $scope.getTeamName = function(team_id){
            var t = $scope.teams.find(team => team.id == team_id);
            return t.teamname;
        }
        $scope.getQuestionName = function(question_id){
            var q = $scope.questions.find(question => question.id == question_id);
            return q.question;
        }
        $scope.getCorrectAnswer = function(question_id){
            var q = $scope.questions.find(question => question.id == question_id);
            return q.correct_answer;
        }

        //todo: return person that is logged in
        $scope.getLoggedinPerson = function(){
            return {id: "2", name:"admin"} ;
        }
    });

