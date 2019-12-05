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
        }).then(function mySuccess(response){
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
            url: "/api/v1.0/answers"
        }).then(function (response){
            $scope.answers = response.data;
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
        /*$scope.updateAnswerCheck = function(answer){
            var data = {"id": answer.id, "correct": answer.correct}
            $http.post("/api/v1.0/updateanswer", JSON.stringify(data))
        }*/
        $scope.getCategoryName = function(category_id){
            categories = $scope.categories;
            //document.write(categories.filter(categories.id == category_id));
            if (category_id in categories)
                return categories[category_id].name;
            return "";
        }
        $scope.getPersonName = function(person_id){
            persons = $scope.persons;
            if (person_id in persons)
               return persons[person_id].username;
            return "";
        }
        //todo: return person that is logged in
        $scope.getLoggedinPerson = function(){
            return {id: "1", name:"postgres"} ;
        }
    });
