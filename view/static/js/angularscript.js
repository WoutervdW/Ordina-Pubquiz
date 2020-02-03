angular.module('module', ['ngRoute'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('//')
        $interpolateProvider.endSymbol('//')
    })
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





        $scope.sortBy = function sortBy(propertyName){
            $scope.reverse = $scope.propertyName === propertyName ? !$scope.reverse : false
            $scope.propertyName = propertyName
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
        r = confirm("Alle antwoorden zullen worden verwijderd. Dit kan niet ongedaan gemaakt worden.")
            if (r == true){
                $http.post("/api/v1.0/reset")
                $scope.answers = [];
            }
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

        $scope.removeOtherStuff = function () {
            $http.post("/api/v1.0/nuke/all")
            window.location.reload()
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
        $scope.fileChanged = function(files) {
             document.getElementById("custom-file-label").innerHTML = files[0].name;
        }

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
    .filter('byCategory', function() {
        return function(answers, category){
            if(answers){
                return answers.filter(function(answer){
                    if(category){
                        return answer.question.questioncategory.name == category;
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



