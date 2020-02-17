angular.module('revealModule', ['ngRoute', 'requestsModule'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('//')
        $interpolateProvider.endSymbol('//')
    })

    .controller('revealcontroller', function ($interval, $filter, httpRequestsService) {
        var vm = this;
        httpRequestsService.getTeams()
        .then(function (response) {
            teams = response.data;
            teams = $filter('orderBy')(teams, 'score', false)
            teams = teams.filter(t => t.score > 0)
        });
        var i = 0
        vm.revealteams = []
        $interval(function () {
            vm.time = vm.time + 1000;
            if (i < teams.length) {
               vm.revealteams.push({
                    "teamname": teams[i].teamname,
                    "score": teams[i].score
                });
                vm.revealteams = $filter('orderBy')(vm.revealteams, 'score', true)
                i += 1;
            }
        }, 4000)
    })