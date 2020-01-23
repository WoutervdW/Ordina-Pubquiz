// define angular interpolationtags as //

angular.module('module', ['ngRoute'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('//')
        $interpolateProvider.endSymbol('//')
    })
    //controller
    .controller('controller', function ($scope, $http, $location, $window, $filter) {
        $http({
            method: "GET",
            url: "/api/v1.0/teams"
        }).then(function (response) {
            $scope.teams = response.data;
        });
        $http({
            method: "GET",
            url: "/api/v1.0/questions"
        }).then(function (response) {
            $scope.questions = response.data;
        });
        $http({
            method: "GET",
            url: "/api/v1.0/categories"
        }).then(function (response) {
            $scope.categories = response.data;
        });
        $http({
            method: "GET",
            url: "/api/v1.0/persons"
        }).then(function (response) {
            $scope.persons = response.data;
        });
        $http({
            method: "GET",
            url: "/api/v1.0/answers"
        }).then(function (response) {
            $scope.answers = response.data;
        });
        $scope.pageNum = 0
        $scope.perPage = 5
        $scope.data = []
        $scope.q = ''
        $scope.numberOfPages = function(){
            if($scope.filteredanswers){
                return Math.ceil($scope.filteredanswers.length / $scope.perPage);
            }
        }

        $scope.newsubanswers = [{}];
        $scope.addField=function(list){
            list.push({});
        }
         $scope.removeField=function(list, obj){
            index = list.indexOf(obj)
            list.splice(index,1)
        }
        $scope.variantsfromsubanswer = function(subanswer){
            if(subanswer.variants){
                variants = subanswer.variants.map(s => s.answer)
                variantsInString = variants.join(" / ")
                return variantsInString;
            }
            return ""
        }
        $scope.sortBy = function sortBy(propertyName){
            $scope.reverse = $scope.propertyName === propertyName ? !$scope.reverse : false
            $scope.propertyName = propertyName
        }
        $scope.addQuestion = function(category_id){
            var newvariants = []
            var subanswers = []
            for (i = 0; i < $scope.newsubanswers.length; i++){
                subanswer = $scope.newsubanswers[i].value
                if(subanswer)
                    variants = subanswer.split('/')
                    for (j = 0; j < variants.length; j++){
                        newvariants.push({"answer": variants[j]})
                    }
                subanswers.push({"variants" : newvariants})
                newvariants = []
            }
            var data = {"questionnumber": $scope.newquestion.questionnumber, "question": $scope.newquestion.question, "subanswers": subanswers, "category": $scope.newquestion.category}
            $http.post("/api/v1.0/newquestion", JSON.stringify(data))
                .then(function (response) {
                if(typeof response.data === 'string'){
                    alert(response.data);
                }
                else{
                    newq = response.data;
                    $scope.questions.push(newq)
                    $scope.newquestion = [];
                    $scope.newsubanswers = [{}]
                }
            })
        }
        $scope.removeQuestion = function (question) {
            var data = {"id": question.id}
            $http.post("/api/v1.0/removequestion", JSON.stringify(data))
                .then (function (response) {
                    if(response.data != 'OK'){
                        alert(response.data)
                    }
                    else{
                        $scope.questions.splice($scope.questions.indexOf(question), 1 );
                    }
                })
        }
        $scope.updateQuestion = function(question){
            for (i = 0; i < question.subanswers.length; i++){
                subanswer = question.subanswers[i].variantsintext
                if(subanswer){
                    question.subanswers[i].variants=[];
                    newvariants=[]
                    variants = subanswer.split('/')
                    for (j = 0; j < variants.length; j++){
                        newvariants.push({"answer": variants[j]})
                    }
                    question.subanswers[i].variants = newvariants
                }
            }
            var data = {"id":question.id, "questionnumber": question.questionnumber, "question": question.question, "subanswers": question.subanswers, "category": question.questioncategory.name}
            $http.post("/api/v1.0/updatequestion", JSON.stringify(data))
            .then(function(response) {
                if(response.data != 'OK'){
                    question.editquestion=true
                    alert(response.data)
                }
            })
        }
        $scope.resetQuestionNumbers = function(){
            for (i = 0; i < $scope.questions.length; i++){
                $scope.questions[i].questionnumber = null;
            }
            $http.post("/api/v1.0/resetquestionnumbers")

        }
        $scope.deleteAllQuestions = function(){
            $http.post("/api/v1.0/deleteallquestions")
             .then(function(response) {
                if(response.data != 'OK'){
                    alert(response.data)
                }
                else{
                    $scope.questions = [];
                }
            })

        }
        $scope.updateAnswerCheck = function (answer) {
            var data = {"id": answer.id, "correct": answer.correct}
            $http
                .post("/api/v1.0/updateanswer", JSON.stringify(data))
                .then(function (response) {
                    answer.checkedby = response.data;
                })
        }

        $scope.deleteAllAnswers = function () {
            $http.post("/api/v1.0/reset")
            $scope.answers = [];
        }
        $scope.checkAllAnswers = function () {
            $scope.checkinganswers = true;
            $http
                .post("/api/v1.0/checkanswers")
                .then(function (response) {
                    $scope.checkinganswers = false;
                    window.location.reload();
                })
        }
        $scope.addTeam = function (team) {
            var data = {"teamname": $scope.newteam}
            $http.post("/api/v1.0/newteam", JSON.stringify(data))
            window.location.reload()
        }
        $scope.removeTeam = function (team) {
            var data = {"id": team.id}
            $http.post("/api/v1.0/removeteam", JSON.stringify(data))
            window.location.reload()
        }
        $scope.removeTeams = function () {
            $http.post("/api/v1.0/removeteams")
            window.location.reload()
        }
        $scope.removeOtherStuff = function () {
            $http.post("/api/v1.0/nuke/all")
            window.location.reload()
        }
        $scope.updateTeam = function (team) {
            var data = {"id": team.id, "teamname": team.teamname}
            $http.post("/api/v1.0/updateteam", JSON.stringify(data))
        }
        $scope.updateAnswerLabel = function () {
            $scope.answersheetform.label = "adsf"
        }
        $scope.showloadingsheetsbar = function () {
            $scope.loadingsheets = true;
        }
        var modal = document.getElementById("myModal");

        $scope.showModal = function () {
            modal.style.display = "block";
        }

        $scope.closeModal = function () {
            modal.style.display = "none";
        }
    })
    .controller('revealcontroller', function ($scope, $http, $interval, $filter) {
        $http({
            method: "GET",
            url: "/api/v1.0/teams"
        }).then(function (response) {
            $scope.teams = response.data;
            $scope.teams = $filter('orderBy')($scope.teams, 'score', false)
        });
        $scope.i = 0
        $scope.revealteams = []
        $interval(function () {
            $scope.time = $scope.time + 1000;
            if ($scope.i < $scope.teams.length) {
                $scope.revealteams.push({
                    "teamname": $scope.teams[$scope.i].teamname,
                    "score": $scope.teams[$scope.i].score
                });
                $scope.revealteams = $filter('orderBy')($scope.revealteams, 'score', true)
                $scope.i = $scope.i + 1;
            }
        }, 4000)
    })

    .controller('pubquizcontroller', function ($scope, $http, $filter, $interval) {
        $http({
            method: "GET",
            url: "/api/v1.0/questions"
        }).then(function (response) {
            $scope.questions = response.data;
            $scope.questions = $scope.questions.filter(q => q.questionnumber > 0
        )
            ;
            $scope.questions = $filter('orderBy')($scope.questions, 'questionnumber', false);
            showQuestions();
        });

        function showQuestions() {
            i = 0;
            var showQuestion = function () {
                if (i < $scope.questions.length) {
                    $scope.displayedquestion = $scope.questions[i];
                    i = i + 1;
                } else {
                    $scope.displayedquestion.questionnumber = "";
                    $scope.displayedquestion.question = "einde pubquiz";
                }
            }
            showQuestion();
            $interval(showQuestion, 300);
        };
    })
    .filter('byTeam', function() {
        return function(answers, team){
            if(answers){
                return answers.filter(function(answer){
                    if(team){
                        return answer.answered_by.teamname == team;
                    }
                    return answer
                })
            }
        }
    })
    .filter('byQuestion', function() {
        return function(answers, question){
            if(answers){
                return answers.filter(function(answer){
                    if(question){
                        return answer.question.question == question.question && answer.question.questionnumber == question.questionnumber;
                    }
                    return answer
                })
            }
        }
    })
    .filter('bySubanswers', function() {
        return function(answers, confidencefrom, confidenceto, correct, checkedby){
            if(answers){
                return answers.filter(function(answer) {
                    filter=false;
                    filteredanswer = answer.subanswersgiven;
                    if(confidencefrom){
                        filter = true;
                        filteredanswer = filteredanswer.filter(function(subanswer){
                            return subanswer.confidence > confidencefrom;
                        })
                    }
                    if(confidenceto){
                        filter = true;
                        filteredanswer = filteredanswer.filter(function(subanswer){
                            return subanswer.confidence < confidenceto;
                        })
                    }
                    if(correct==true){
                        filter = true;
                        filteredanswer = filteredanswer.filter(function(subanswer){
                            return subanswer.correct == true;
                        })
                    }
                    if(correct==false){
                        filter = true;
                        filteredanswer = filteredanswer.filter(function(subanswer){
                            return subanswer.correct == false;
                        })
                    }
                    if(checkedby){
                        filter = true;
                        filteredanswer = filteredanswer.filter(function(subanswer){
                            return subanswer.checkedby.personname == checkedby;
                        })
                    }
                    if(filteredanswer.length>0){
                        return answer;
                    }
                })
            }
        }
    })
    .filter('byConfidence', function () {
        return function (subanswers, confidencefrom, confidenceto) {
            if (!confidencefrom && !confidenceto) {
                return subanswers;
            } else if (!confidencefrom) {
                return subanswers.filter(function (subanswer) {
                    return subanswer.confidence < confidenceto;
                })
            } else if (!confidenceto) {
                return subanswers.filter(function (subanswer) {
                    return subanswer.confidence > confidencefrom;
                })
            } else {
                return subanswers.filter(function (subanswer) {
                    return subanswer.confidence > confidencefrom && subanswer.confidence < confidenceto;
                })
            }
        }
    })
    .filter('byCorrect', function () {
        return function (subanswers, correctfilter) {
            return subanswers.filter(function (subanswer){
                if(correctfilter==true){
                    return subanswer.correct;
                }
                else if(correctfilter==false){
                    return !subanswer.correct;
                }
                else{
                    return subanswer;
                }
            })
        }
    })
    .filter('byChecked', function () {
        return function (subanswers, checkedfilter) {
            return subanswers.filter(function (subanswer){
                if(checkedfilter){
                    return subanswer.checkedby.personname==checkedfilter;
                }
                else{
                    return subanswer;
                }
            })
        }
    })
    .filter('pagination', function () {
        return function (input, page, perPage) {
            if(input){
                return input.slice(page*perPage, (page+1) * perPage);
            }
        }
    });


