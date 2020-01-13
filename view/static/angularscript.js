// define angular interpolationtags as //

angular.module('module', ['ngRoute'])
    .config(function($interpolateProvider){
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
        $scope.currentPage = 0;
        $scope.pageSize = 10;
        $scope.data = [];
        $scope.q = '';
        $scope.numberOfPages = function(){
            return Math.ceil($scope.subanswers.length / $scope.pageSize);
        }

        $scope.newsubanswers = [{}];
        $scope.addField=function(){
              $scope.newsubanswers.push({});
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
            var data = {"questionnumber": $scope.newquestionnumber, "question": $scope.newquestion, "subanswers": subanswers, "category": $scope.newquestioncategory, "active": $scope.newquestionactive};
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
            .then(function(response) {
                alert(response.data)
            })
        }
        $scope.updateAnswerCheck = function(answer){
            var data = {"id": answer.id, "correct": answer.correct}
            $http.post("/api/v1.0/updateanswer", JSON.stringify(data))
        }
        $scope.deleteAllAnswers = function(){
            $http.post("/api/v1.0/reset")
        }
        $scope.checkAllAnswers = function(){
            $scope.checkinganswers = true;
            $http
            .post("/api/v1.0/checkanswers")
            .then(function (response) {
                $scope.checkinganswers = false;
                window.location.reload();
            })
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
        $scope.updateAnswerLabel = function(){
            $scope.answersheetform.label = "adsf";
        }
        $scope.showloadingsheetsbar = function(){
            $scope.loadingsheets = true;
        }
    })

    .controller('revealcontroller', function($scope, $http, $interval, $filter){
        $http({
            method: "GET",
            url: "/api/v1.0/teams"
        }).then(function (response){
            $scope.teams = response.data;
            $scope.teams = $filter('orderBy')($scope.teams, 'score', false)
        });
        $scope.i = 0;
        $scope.revealteams = [];

        $interval( function(){
        $scope.time = $scope.time + 1000;
            if ($scope.i < $scope.teams.length){
                $scope.revealteams.push({"teamname": $scope.teams[$scope.i].teamname, "score":$scope.teams[$scope.i].score});
                $scope.revealteams = $filter('orderBy')($scope.revealteams, 'score', true)
                $scope.i =  $scope.i + 1;
            }
        }, 4000);
    })
    .controller('pubquizcontroller', function($scope, $http, $filter, $interval){
        $http({
            method: "GET",
            url: "/api/v1.0/questions"
        }).then(function (response){
            $scope.questions = response.data;
            $scope.questions = $scope.questions.filter(q => q.questionnumber  > 0);
            $scope.questions = $filter('orderBy')($scope.questions, 'questionnumber', false);
            showQuestions();
        });

        function showQuestions(){
        i = 0;
            var showQuestion = function(){
                if (i < $scope.questions.length){
                $scope.displayedquestion = $scope.questions[i];
                i =  i + 1;
                }
                else{
                    $scope.displayedquestion.questionnumber = "";
                    $scope.displayedquestion.question = "einde pubquiz";

                }
            }
        showQuestion();
        $interval(showQuestion, 300);
        };
    })

    .filter('byConfidence', function(){
        return function(subanswers, confidencefrom, confidenceto){
            if (!confidencefrom && !confidenceto){
                return subanswers;
            }
            else if (!confidencefrom){
                return subanswers.filter(function (subanswer){
                     return subanswer.confidence < confidenceto;
                })
            }
            else if (!confidenceto){
                return subanswers.filter(function (subanswer){
                     return subanswer.confidence > confidencefrom;
                })
            }
            else{
                return subanswers.filter(function (subanswer){
                      return subanswer.confidence > confidencefrom && subanswer.confidence < confidenceto;
                })
            }
        }
    })
    .filter('startFrom', function() {
        return function(input, start) {
            start = +start;
            return input.slice(start);
        }
    });

