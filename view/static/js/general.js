angular.module('generalModule', [])
    .factory('generalService', function(){
        vm = this
        return{
            sortBy: function (reverse, currentPropertyName, propertyName){
                reverse = currentPropertyName === propertyName ? !reverse : false
                currentPropertyName = propertyName
                return [reverse, currentPropertyName]
            }
        }
    });