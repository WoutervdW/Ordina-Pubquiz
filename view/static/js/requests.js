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
            }
        }
    })
