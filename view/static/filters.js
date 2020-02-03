angular.filter('byTeam', function() {
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
filter('byCategory', function() {
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
angular.filter('byQuestion', function() {
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
angular.filter('bySubanswers', function() {
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
angular.filter('byConfidence', function () {
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
angular.filter('byCorrect', function () {
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
angular.filter('byChecked', function () {
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
