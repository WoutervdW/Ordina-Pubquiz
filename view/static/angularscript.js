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
          //  document.write(JSON.stringify($scope.questions[3]));
        });
       /* $http({
            method: "GET",
            url: "/api/v1.0/subanswers"
        }).then(function (response){
            $scope.subanswers = response.data;
        });
        */
      /*  $http({
            method: "GET",
            url: "/api/v1.0/variants"
        }).then(function (response){
            $scope.variants = response.data;
        });
        */
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
       /* $http({
            method: "GET",
            url: "/api/v1.0/subanswersgiven"
        }).then(function (response){
            $scope.subanswersgiven = response.data;
        });*/
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
            for (i = 0; i < $scope.newsubanswers.length; i++){
                subanswer = $scope.newsubanswers[i].value;
                variants = subanswer.split('/');
                newvariants.push(variants);
            }
            $scope.questions.variants = newvariants;
            $scope.subanswers.push($scope.newsubanswers);
            $scope.newsubanswers = [{}];
            var data = {"question": $scope.newquestion, "subanswers": $scope.subanswers, "category_id": $scope.newquestioncategory, "person_id": $scope.getLoggedinPerson().id, "active":$scope.newquestionactive};
            $http.post("/api/v1.0/newquestion", JSON.stringify(data))
            $scope.questions.push(data);
            $scope.newquestion = "";
       }
       $scope.updateQuestionActive = function(question){

            var data = {"id":question.id, "active":question.active}
            $http.post("/api/v1.0/updatequestion", JSON.stringify(data))
       }
       $scope.updateAnswerCheck = function(answer){
            var data = {"id": answer.id, "correct": answer.correct, "person_id":$scope.getLoggedinPerson().id}
            $http.post("/api/v1.0/updateanswer", JSON.stringify(data))
       }
       
        //todo: return person that is logged in
        $scope.getLoggedinPerson = function(){
            return {id: "2", name:"admin"} ;
        }
    });


