angular.module('questionModule', ['ngRoute','requestsModule', 'generalModule'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('//')
        $interpolateProvider.endSymbol('//')
    })
    .controller('questionController', function ($http, httpRequestsService, generalService) {
        var vm = this
        httpRequestsService.getQuestions()
        .then(function (response) {
            vm.questions = response.data
        });

         httpRequestsService.getCategories()
        .then(function (response) {
            vm.categories = response.data
        });

        vm.newsubanswers = [{}]

        vm.addField=function(list){
            list.push({});
        }

        vm.removeField=function(list, obj){
            index = list.indexOf(obj)
            list.splice(index,1)
        }

        vm.addQuestion = function(category_id){
            var newvariants = []
            var subanswers = []
            for (i = 0; i < vm.newsubanswers.length; i++){
                subanswer = vm.newsubanswers[i].value
                if(subanswer)
                    variants = subanswer.split('/')
                    for (j = 0; j < variants.length; j++){
                        newvariants.push({"answer": variants[j]})
                    }
                subanswers.push({"variants" : newvariants})
                newvariants = []
            }

            var data = {"questionnumber": vm.newquestion.questionnumber, "question": vm.newquestion.question, "subanswers": subanswers, "category": vm.newquestion.category}
            httpRequestsService.addQuestion(JSON.stringify(data))
            .then(function (response) {
                if(typeof response.data === 'string'){
                    alert(response.data)
                }
                else{
                    newq = response.data;
                    vm.questions.push(newq);
                    vm.newquestion = [];
                    vm.newsubanswers = [{}]
                }
            })
        }

        vm.removeQuestion = function (question) {
            var data = {"id": question.id}
            httpRequestsService.removeQuestion(JSON.stringify(data))
            .then (function (response) {
                if(response.data != 'OK'){
                    alert(response.data)
                }
                else{
                    vm.questions.splice(vm.questions.indexOf(question), 1 )
                }
            })
        }

        vm.updateQuestion = function(question){
            for (i = 0; i < question.subanswers.length; i++){
                subanswer = question.subanswers[i].variantsintext
                if(subanswer){
                    question.subanswers[i].variants=[]
                    newvariants=[]
                    variants = subanswer.split('/')
                    for (j = 0; j < variants.length; j++){
                        newvariants.push({"answer": variants[j]})
                    }
                    question.subanswers[i].variants = newvariants
                }
            }
            var data = {"id":question.id, "questionnumber": question.questionnumber, "question": question.question, "subanswers": question.subanswers, "category": question.questioncategory.name}
            httpRequestsService.updateQuestion(JSON.stringify(data))
            .then(function(response) {
                if(response.data != 'OK'){
                    question.editquestion=true
                    alert(response.data)
                }
            })
        }

        vm.resetQuestionNumbers = function(){
            r = confirm("Alle vraagnummers worden gereset. Dit kan niet ongedaan gemaakt worden.")
            if (r == true){
                for (i = 0; i < vm.questions.length; i++){
                    vm.questions[i].questionnumber = null
                }
                httpRequestsService.resetQuestionNumbers()
            }
        }

        vm.deleteAllQuestions = function(){
            r = confirm("Alle vragen zullen worden verwijderd. Dit kan niet ongedaan gemaakt worden.")
            if (r == true){
                httpRequestsService.deleteAllQuestions()
                .then(function(response) {
                    if(response.data != 'OK'){
                        alert(response.data)
                    }
                    else{
                        vm.questions = []
                    }
                })
            }
        }

        vm.variantsfromsubanswer = function(subanswer){
            if(subanswer.variants){
                variants = subanswer.variants.map(s => s.answer)
                variantsInString = variants.join(" / ")
                return variantsInString;
            }
            return ""
        }

        vm.deleteCategory = function(category) {
            var data = {"id": category.id}
            httpRequestsService.deleteCategory(JSON.stringify(data))
                .then(function(response){
                    if(response.data !== 'OK'){
                        alert(response.data)
                    }
                    else{
                        vm.categories.splice(vm.categories.indexOf(category), 1 );
                    }
                })
        }

        vm.sortBy = function(propertyName){
            result = generalService.sortBy(vm.reverse, vm.propertyName, propertyName)
            vm.reverse = result[0]
            vm.propertyName = result[1]
        }

        vm.createDoc = function(){
            vm.creatingFile = true;
            data = []
            if(vm.breaks){
                for (i = 0; i < vm.breaks.length; i++)
                    data.push(vm.breaks[i].breaknumber)
            }
            httpRequestsService.createDoc(data)
            .then (function (response) {
                alert(response.data)
                vm.creatingFile=false;
            })
        }
        vm.updateBreaks = function(){
            vm.breaks = []
            for (i = 0; i < vm.amountOfBreaks; i++){
                vm.breaks.push({})
            }
        }
    })
