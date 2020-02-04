angular.module('requestsModule', [])
    .factory('httpRequestsService', function($http){
        return{
            getQuestions: function (){
                return  $http({
                    method: "GET",
                    url: "/api/v1.0/questions"
                })
            },
            getTeams: function(){
                return $http({
                    method: "GET",
                    url: "/api/v1.0/teams"
                })
            },
            getCategories: function(){
                return $http({
                    method: "GET",
                    url: "/api/v1.0/categories"
                })
            },

            addQuestion: function(question){
                 return $http.post("/api/v1.0/newquestion", question)
            },

            removeQuestion: function(question){
                 return $http.post("/api/v1.0/removequestion", question)

            },

            deleteAllQuestions: function(){
                return $http.post("/api/v1.0/deleteallquestions")
            },

            updateQuestion: function(question){
                return $http.post("/api/v1.0/updatequestion", question)
            },

            resetQuestionNumbers: function(){
                $http.post("/api/v1.0/resetquestionnumbers")
            },

            deleteCategory: function(category){
                return $http.post("/api/v1.0/removecategory", category)
            },

            createDoc: function(document){
                return $http.post("/api/v1.0/createdoc", document)
            },

            addTeam: function(team){
                return $http.post("/api/v1.0/newteam", team)
            },

            removeTeam: function(team){
                $http.post("/api/v1.0/removeteam", team)
            },

            updateTeam: function(team){
                $http.post("/api/v1.0/updateteam", team)
            }

        }
    })
