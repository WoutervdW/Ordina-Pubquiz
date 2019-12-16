// define angular interpolationtags as {a a}
angular.module('module', ['ngRoute'])
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
    })
    //controller
    .controller('controller', function($scope, $http, $location, $window){
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
            url: "/api/v1.0/subanswers"
        }).then(function (response){
            $scope.subanswers = response.data;
        });

        $scope.newsubanswers = [{}];
        $scope.addField=function(){
              $scope.newsubanswers.push({})
        }
        $scope.sortBy = function sortBy(propertyName){
              $scope.reverse = $scope.propertyName === propertyName ? !$scope.reverse : false;
              $scope.propertyName = propertyName;
        }
        $scope.addQuestion = function(category_id){
          var newvariants = [];
          var subanswers = [];
          for (i = 0; i < $scope.newsubanswers.length; i++){
                subanswer = $scope.newsubanswers[i].value;
                variants = subanswer.split('/');
                for (j = 0; j < variants.length; j++){
                    newvariants.push({"answer": variants[j]});
                }
                subanswers.push({"variants" : newvariants});
                newvariants = [];
            }
            $scope.newsubanswers = [{}];
            var data = {"question": $scope.newquestion, "subanswers": subanswers, "category": $scope.newquestioncategory, "person_id": $scope.getLoggedinPerson().id, "active":$scope.newquestionactive};
            $http.post("/api/v1.0/newquestion", JSON.stringify(data))
            $scope.newquestion = "";
            window.location.reload();
        }
        $scope.removeQuestion = function(question){
            var data = {"id":question.id}
            $http.post("/api/v1.0/removequestion", JSON.stringify(data))
            window.location.reload();
        }
        $scope.updateQuestionActive = function(question){
            var data = {"id":question.id, "active":question.active}
            $http.post("/api/v1.0/updatequestion", JSON.stringify(data))
        }
        $scope.updateQuestionNumber = function(question){
            var data = {"id":question.id, "questionnumber": question.questionnumber}
            $http.post("/api/v1.0/updatequestion", JSON.stringify(data))

        }
        $scope.updateAnswerCheck = function(answer){
            var data = {"id": answer.id, "correct": answer.correct, "person_id":$scope.getLoggedinPerson().id}
            $http.post("/api/v1.0/updateanswer", JSON.stringify(data))
        }
        $scope.deleteAllAnswers = function(){
            $http.post("/api/v1.0/reset")
        }
        $scope.addTeam = function(team){
            var data = {"teamname":$scope.newteam}
            $http.post("/api/v1.0/newteam", JSON.stringify(data))
            window.location.reload();
        }
        $scope.removeTeam = function(team){
            var data = {"id":team.id}
            $http.post("/api/v1.0/removeteam", JSON.stringify(data))
            window.location.reload();
        }
          $scope.removeTeams = function(){
            $http.post("/api/v1.0/removeteams")
            window.location.reload();
        }

        $scope.login = function(){
            var data = {"username": $scope.username, "password": $scope.password}
            $http.post("/login", JSON.stringify(data))
        }

        //todo: return person that is logged in
        $scope.getLoggedinPerson = function(){
            return {id: "2", personname:"admin"} ;
        }
    });

