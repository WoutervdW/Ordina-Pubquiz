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
            //teams = teams.filter(t => t.score > 0)
        });
        var i = 0;
        vm.revealteams1 = [];
        vm.revealteams2 = [];
        vm.revealteams3 = [];
        vm.revealteams4 = [];
        $interval(function () {
            vm.time = vm.time + 1000;
            if (i < teams.length) {
                if (i < teams.length / 4){
                    vm.revealteams1.insert(0, {
                        "position": teams.length - i,
                        "teamname": teams[i].teamname,
                        "score": teams[i].score
                    })
                }
                if (i >= teams.length / 4 && i < 2 * teams.length / 4){
                    vm.revealteams2.insert(0, {
                        "position": teams.length - i,
                        "teamname": teams[i].teamname,
                        "score": teams[i].score
                    })
                }
                if (i >= 2 * teams.length / 4 && i < 3 * teams.length / 4){
                    vm.revealteams3.insert(0, {
                        "position": teams.length - i,
                        "teamname": teams[i].teamname,
                        "score": teams[i].score
                    })
                }
                if (i >= 3 * teams.length / 4){
                    vm.revealteams4.insert(0, {
                        "position": teams.length - i,
                        "teamname": teams[i].teamname,
                        "score": teams[i].score
                    })
                }
                i += 1;
            }
        }, 2000)
    })


Array.prototype.insert = function ( index, item ) {
    this.splice( index, 0, item );
};
