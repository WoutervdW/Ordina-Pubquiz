angular.module('answerCheckingModule')
    .filter('startFrom', function() {
        return function(input, start) {
            start = +start; //parse to int
            return input.slice(start);
        }
    })

    .filter('pagination', function () {
        vm.currentPage = 0;
        return function (input, page, perPage) {
            if(input){
                return input.slice(page*perPage, (page+1) * perPage);
            }
        }
    });



