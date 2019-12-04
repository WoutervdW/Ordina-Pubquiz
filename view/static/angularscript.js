
// define angular interpolationtags as {a a}
angular.module('module', [])
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
    })
    //controller for index.html
    .controller('indexcontroller', function($scope, $http){
        $http({
            method: "GET",
            url: "/api/v1.0/teams"
        }).then(function mySuccess(response){
            $scope.teams = response.data;
        });
        $scope.propertyName = 'score';
        $scope.reverse = 'false';
        $scope.sortBy = function(propertyName) {
            $scope.reverse = $scope.propertyName === propertyName ? !$scope.reverse : false;
            $scope.propertyName = propertyName;
        }
    })

    //controller for questions.html
    .controller('questionscontroller', function($scope, $http){
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
            url: "/api/v1.0/users"
        }).then(function (response){
            $scope.users = response.data;
        });
        $scope.propertyName = 'question';
        $scope.reverse = 'false';
        $scope.sortBy = function(propertyName) {
            $scope.reverse = $scope.propertyName === propertyName ? !$scope.reverse : false;
            $scope.propertyName = propertyName;
        }
        $scope.addQuestion = function(){
            var data = {"question": $scope.newquestion, "correct_answer": $scope.newquestioncorrect_answer, "category_id": "1", "user_id": "1", "active":$scope.newquestionactive};
            $http.post("/api/v1.0/newquestion", JSON.stringify(data))
            $scope.questions.push(data);
            $scope.newquestion = "";
            $scope.newquestioncorrect_answer = "";
        };
        $scope.updateQuestionActive = function(questionid, active){
            currentquestion = $scope.questions.find(x => x.id === questionid)
            var data = {"id":currentquestion.id, "active":active}
            $http.post("/api/v1.0/updatequestion", JSON.stringify(data))
        }
        $scope.getCategoryName = function(category_id){
            categories = $scope.categories;
            if (category_id in categories)
                return (categories[category_id]).name;
            return "";
        }
        $scope.getUserName = function(user_id){
            users = $scope.users;
            if (user_id in users)
                return users[user_id].username;
            return "";
        }
        //todo: return user that is logged in
        $scope.getCurrentUser = function(){
            return {id: "1", name:"postgres"} ;
        }
    });
