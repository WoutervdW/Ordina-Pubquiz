angular.module('indexModule', ['ngRoute', 'requestsModule', 'generalModule'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('//')
        $interpolateProvider.endSymbol('//')
    })
   .controller('indexController', function ($http, $filter, $interval, httpRequestsService, generalService){
        var vm = this
        httpRequestsService.getTeams()
        .then(function (response) {
            vm.teams = response.data;
        });
        vm.addTeam = function (team) {
            var data = {"teamname": vm.newteam}
            $http.post("/api/v1.0/newteam", JSON.stringify(data))
            .then(function(response){
                newt = response.data;
                vm.teams.push(newt)
                vm.newteam=""
            })
        }
        vm.removeTeam = function (team) {
            var data = {"id": team.id}
            $http.post("/api/v1.0/removeteam", JSON.stringify(data))
            vm.teams.splice(vm.teams.indexOf(team), 1);
        }
        vm.removeTeams = function () {
            $http.post("/api/v1.0/removeteams")
            vm.teams=[]
        }
        vm.updateTeam = function (team) {
            var data = {"id": team.id, "teamname": team.teamname}
            vm.teams.indexOf(team).teamname = team.teamname
            $http.post("/api/v1.0/updateteam", JSON.stringify(data))
        }
        vm.sortBy = function(propertyName){
            result = generalService.sortBy(vm.reverse, vm.propertyName, propertyName)
            vm.reverse = result[0]
            vm.propertyName = result[1]
        }
   })