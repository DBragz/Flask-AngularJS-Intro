/**
 * 
 * @questionController.js
 * Controls the main page of the mainApp application.
 *
 * The controller for mainApp where it handles the 
 * functionality of how the user inseracts with the 
 * questions.  
 * 
 */

//  Creating the questionController in order to manipulate the main page.
mainApp.controller("questionController", function($scope, httpService) {
    
    'use scrict'
    
    //These values are constants and will never change
    server = 'http://127.0.0.1:5000'
    validQuestionExp = /^[0-9a-zA-Z+-/* ?]+$/
    validDistractorsExp = /^[0-9]+(,[0-9]+)*$/
    QUESTION = 0
    ANSWER = 1
    DISTRACTORS = 2
    ANSWERGREATER = 3
    ANSWERLESS = 4
    EQUALSTRING = 'EQUALS'
    GREATERSTRING = 'GREATER'
    LESSSTRING = 'LESS'
    rowSize = 5
    OK = 200
    INTERNALERR = 400
    
    //Values will change based on website state
    $scope.submitBtn = 'Insert Question'
    $scope.insertMode = true
    globalList = []
    currentId = null
    currentPage = 1
    
    
   /**
    *
    * Initilizes the page by grabbing all of 
    * the questions from the server.
    *
    */
    
    $scope.init = function() {   
        $scope.getAllQs()
    }
      
      
   /**
    * 
    * Makes a call to the server to grab 
    * all of the questions currently available.
    * 
    */
      
    $scope.getAllQs = function(){
        
        currentPage = 1
        httpService.getRequest(server + '/getquestions',{},$scope.getAllQsResponse)
        $scope.clearInput()
        
    };

    
   /**
    *
    * Updates the page based on the information 
    * recieved from the get questions http call.
    *
    * @param {response} response
    *   Response from the server after call 
    *   get all questions.
    * 
    */
    
    $scope.getAllQsResponse = function(response){
        
        if(response && response.data && response.data.code && response.data.code == OK){
           
            globalList = $scope.convertResponseToJson(response)
            
            if(globalList.length != 0){
                $scope.displayTable(1)
            }
            else{
                $scope.setTableToEmpty()
            }
        }
        else if(response && response.data && response.data.code && response.data.code == INTERNALERR){
            alert(response.data.text)
        }
        else{
            alert("An unknown error has occurred: Unable to Get Questions")
            
        }
        
    };
    
    
   /**
    * 
    * Makes a call to the server to delete
    * a specific question.
    * 
    */
    
    $scope.deleteQ = function(qid){
         
        question = { 'questionid':qid }
        
        httpService.deleteRequest(server + '/deletequestion',question,$scope.deleteQResponse)
        
    };
    
    
   /**
    * 
    * Updates the page based on the information 
    * recieved from the delete question request.
    *
    * @param {response} response
    *   Response from the server after call 
    *   to delete a specific questions.
    * 
    */
    
    $scope.deleteQResponse = function(response){
         
        if(response && response.data && response.data.code && response.data.code == OK &&
            response.data.success && response.data.success == true ){
          
            jsonQuestion = JSON.parse(response.data.list[0])
            
            $scope.removeQuestion(jsonQuestion.questionid)
            
            if( (globalList.length / rowSize < currentPage) && globalList.length % rowSize == 0 && currentPage != 1){
                currentPage--
            }
            
            $scope.displayTable(currentPage)
           
        }
        else if(response && response.data && response.data.code && response.data.code == INTERNALERR){
            alert(response.data.text)
        }
        else{
            alert("An unknown error has occurred: Unable to Delete Questions")
            
        }
             
    };
    
    
   /**
    * 
    * Hanldes the input button input boxes
    * in order to insert or update a question 
    * based on what mode it is in.
    *
    * @param {question} string
    *   A question string to insert or update a question
    * @param {answer} integer
    *   Integer value to insert or update a question 
    * @param {distractors} string
    *   A string list of integers to insert or update a question
    *
    */
    
    $scope.handleInputButton = function(question, answer, distractors){
        
        stringDistractors = String(distractors)
        
        if($scope.insertMode){
            
            if($scope.checkQuestionInput(question, answer, distractors)){
            
                question = { 'question':question, 
                    'answer':answer, 'distractors':stringDistractors.replace(/\s+/g,'') }

                httpService.postRequest(server + '/insertquestion' ,question,$scope.insertQResponse)
            }
        }
        else{
        
                
            if($scope.checkQuestionInput(question, answer, distractors)){
            
                question = { 'questionid':currentId, 'question':question, 
                    'answer':answer, 'distractors': stringDistractors.replace(/\s+/g,'') }
                
                httpService.postRequest(server + '/updatequestion',question, $scope.updateQResponse)
                
            }

            $scope.insertModeSet(true)
            
        }
        
        $scope.clearInput()
    
    };
    
    
   /**
    * 
    * Updates the page based on the information 
    * recieved from the insert question request.
    *
    * @param {response} response
    *   Response from the server after call 
    *   to insert a specific questions.
    * 
    */
    
    $scope.insertQResponse = function(response){
         
        if(response && response.data && response.data.code && response.data.code == OK &&
            response.data.success && response.data.success == true ){
          
            jsonQuestion = JSON.parse(response.data.list[0])
            
            $scope.addQuestion(jsonQuestion.questionid, jsonQuestion.question, 
                jsonQuestion.answer, jsonQuestion.distractors)
           
            $scope.getAllQs()
           
        }
        else if(response && response.data && response.data.code && response.data.code == INTERNALERR){
            alert(response.data.text)
        }
        else{
            alert("An unknown error has occurred: Unable to Insert Questions")
            
        }
        
    };
    
    
   /**
    * 
    * Updates the page based on the information 
    * recieved from the update question request.
    *
    * @param {response} response
    *   Response from the server after call 
    *   to update a specific questions.
    * 
    */
        
    $scope.updateQResponse = function(response){
        
        
        if(response && response.data && response.data.code && response.data.code == OK &&
            response.data.success && response.data.success == true ){
          
            jsonQuestion = JSON.parse(response.data.list[0])
            
            $scope.updateQuestion(jsonQuestion.questionid, jsonQuestion.question, 
                jsonQuestion.answer, jsonQuestion.distractors)
           
        }
        else if(response && response.data && response.data.code && response.data.code == INTERNALERR){
            alert(response.data.text)
        }
        else{
            alert("An unknown error has occurred: Unable to Update Questions")
            
        }
        
    };
    
    
   /**
    *
    * Creates the request to check if question, answer, 
    * or distractor contains a specific value.
    *
    * @param {integer} value
    *   The value used to indicate what propety is being 
    *   used to compare.
    * @param {string} string
    *   The value being used to compare
    * 
    */
    
    $scope.getQuestionsWhereContains = function(value, string){
    
    
        if(string = $scope.checkContainsInput(value,string)){
            
            question = {}
            url = '/getquestionsfrom'
            
            if(QUESTION == value){
                
                question = {'question': string}
                
                url += 'question'
                
            }
            else if(ANSWER == value || ANSWERGREATER == value || ANSWERLESS == value){
                
                condition = ''
                
                if(value == ANSWER){
                    condition = EQUALSTRING
                }
                else if(value == ANSWERGREATER){
                    condition = GREATERSTRING
                }
                else if(value == ANSWERLESS){
                    condition = LESSSTRING
                }
                else{
                    alert('Invalid Input: Unable to make contains call')
                }
            
                if(condition){
                    
                    question = {'answer': string, 'condition': condition}
                    
                    url += 'answer'
                }
                
            }
            else if(DISTRACTORS == value){
                
                question = {'distractors': string}
                
                url += 'distractors'
                
            }
            else{
                alert('Unable to create url')
            }
            
            httpService.getRequest(server + url,
                    question, $scope.getQuestionsWhereContainsResponse)
            
            
        }
        
    };
    
    
   /**
    *
    * Updates the page based on the information 
    * recieved from the question property contains 
    * request.
    *
    * @param {response} response
    *   Response from the server after call 
    *   to get if question contains a specific
    *   property.
    * 
    */
    
    $scope.getQuestionsWhereContainsResponse = function(response){
        
        $scope.clearInput()
        
        if(response && response.data && response.data.code && response.data.code == OK &&
            response.data.success && response.data.success == true ){
            
            globalList = $scope.convertResponseToJson(response)
            
            if(globalList.length != 0){
                 $scope.displayTable(1)
            }
            else{
                $scope.setTableToEmpty()
            }
            
        }
        else if(response && response.data && response.data.code && response.data.code == INTERNALERR){
            alert(response.data.text)
        }
        else{
            alert("An unknown error has occurred: Unable to Update Questions")
            
        }
        
    };

    
   /**
    * 
    * Checks the string value to see if valid.
    *
    * @param {value} value
    *   The value for what property is being 
    *   checked.
    * @param {string} string
    *   The string to check to see if it 
    *   is valid.
    * 
    * @return {boolean} 
    *   Returns true if input is valid.
    */
    
    $scope.checkContainsInput = function(value, string){
        
        if(string){
        
            if(QUESTION == value){
                 
                questionValid = validQuestionExp.test(string)
                
                andValid = string.indexOf('&') > -1
                
                 if(questionValid && !andValid){
                        return string
                 }
                 else{
                    alert('Invalid Input: Make sure to check only valid characters for Questions')
                 }
                   
            }
            else if(ANSWER == value || ANSWERGREATER == value || ANSWERLESS == value){
                
                isInt = (NaN != parseInt(string))
                isNotDouble = (string.indexOf('.') == -1)
                
                if(isInt && isNotDouble){
                    return string
                }
                else{
                    alert('Invalid Input: Answer is not an integer')
                }
                
            }
            else if(DISTRACTORS == value){
                
                    string = string.replace(/\s+/g,'')
                
                    distractorsValid = validDistractorsExp.test(string)
                
                    isNotDouble = (string.indexOf('.') == -1)
                    
                    if(distractorsValid && isNotDouble){
                        return string
                    }
                    else{
                        alert('Invalid Input: Make sure sure Distractor is valid and all numbers are integers')
                    }
            }            
            else{
                alert('Invalid Input: Unable to identify question property to check for contains')
            }
        }
        else{
            alert('Invalid Input: Nothing to check in contains input box')
        }
        return false
    }
    
   /**
    * 
    * Checks the question values to see if valid.
    *
    * @param {string} question
    *   The question property being checked to 
    *   see if it is valid
    * @param {string} answer
    *   The answer property being checked to 
    *   see if it is valid
    * @param {string} distractor
    *   The distractors property being checked to 
    *   see if it is valid
    * 
    * @return {boolean} 
    *   Returns true if input is valid.
    *
    */
    
    $scope.checkQuestionInput = function(question, answer, distractor) {
        
        stringDistractor = String(distractor).replace(/\s+/g,'')
        
        if(question && answer && stringDistractor){
            
            questionValid = validQuestionExp.test(question)
            
            andValid = question.indexOf('&') > -1
            
            distractorsValid = validDistractorsExp.test(stringDistractor)
            
            if(questionValid && !andValid){
                if(distractorsValid){
                    return true
                }
                else{
                    alert('Invalid Input: Make sure Distractors string is valid')
                }
            }
            else{
                alert('Invalid Input: Make sure Question is valid and does not contain & symbol')
            }
        }
        else{
            alert('Invalid Input')
        }
        
        return false
        
    }
    
   /**
    * 
    * Clears the input boxes.
    * 
    */
    
    $scope.clearInput = function(){
        
        $scope.questionInput = ''
        $scope.answerInput = ''
        $scope.distractorsInput = ''
        $scope.containsInput = ''
        
    }
    
    
   /**
    * 
    * Checks the question values to see if valid.
    *
    * @param {integer} questionid
    *   The questionid that will be used to update
    *   the other properties.
    * @param {string} question
    *   The question property of the question 
    *   used to update the current question.
    * @param {integer} answer
    *   The answer property of the question 
    *   used to update the current question.
    * @param {string} distractors
    *   The distractors property of the question 
    *   used to update the current question.
    */
    
    $scope.updateInput = function(questionid, question, answer, distractors){
        
        $scope.insertMode = false
        
        $scope.questionInput = question
        $scope.answerInput = parseInt(answer)
        $scope.distractorsInput = distractors
        
        currentId = questionid
        
        $scope.submitBtn = 'Update Question'
        
    };

    
   /**
    * 
    *   Goes to the next page of questions.
    *
    */
    
    $scope.nextPage = function(){        
        
        startSize = currentPage * 5
        endSize = (currentPage + 1) * 5
        
        if(globalList.length > startSize){
            currentPage++
            $scope.displayTable(currentPage)
        }
        else{
            alert('No more Questions in database.')
        }
    }

    
   /**
    * 
    *   Goes to the previous page of questions.
    *
    */
    
    $scope.previousPage = function(){
        
        if(currentPage != 1){
            currentPage--
            $scope.displayTable(currentPage)
        }
        else{
            alert('You are at the begining of the Questions list.')
        }
    }
    
    
   /**
    * 
    *   Sets the pages to an empty table view.
    *
    */
    
    $scope.setTableToEmpty = function(){
        
        globalList = []
        $scope.listView = []
        
    }
    
    
   /**
    * 
    *   Displays the current page of questions.
    *
    * @param {integer} page
    *   The page to update the view on what 
    *   questions to show.
    *
    */
    
    $scope.displayTable = function(page){
        
        endList = page * rowSize
        startList = endList - rowSize
        
        $scope.listView = globalList.slice(startList,endList)
        
    };
    
    
   /**
    * 
    *   Removes the question from the view.
    *
    * @param {integer} id
    *   The questionid to remove from the table.
    *
    */
    
    $scope.removeQuestion = function(id) {
        for (i in globalList) {
            if (globalList[i].questionid == id) {
                globalList.splice(i, 1);
                $scope.clust = {};
            }
        }
    }
    
    
   /**
    * 
    *   Updates the mode of the application from 
    *   insert question mode to update question mode.
    *
    * @param {boolean} value
    *   True if in insert mode, false if in update mode. 
    *
    */
    
    $scope.insertModeSet = function(value){
        
        insertMode = value
        if(value){
            $scope.submitBtn = 'Insert Question'
            currentId = null
        }
        else{ 
            $scope.submitBtn = 'Insert Question'
        }
        
        $scope.insertMode = value
    
    }
    
    
   /**
    * 
    * Updates the view by adding a question to the table.
    *
    * @param {integer} questionid
    *   The questionid property used to insert in the question.
    * @param {string} question
    *   The question property used to insert in the question.
    * @param {integer} answer
    *   The answer property used to insert in the question.
    * @param {string} distractors
    *   The distractors property used to insert in the question.
    */
    
    $scope.addQuestion = function(questionid, question, answer, distractors){
        
        globalList.push({questionid:questionid, question:question, answer:answer, distractors: distractors})
        
        $scope.displayTable(currentPage)
        
    }
    
    
   /**
    * 
    * Updates the view by adding a question to the table.
    *
    * @param {integer} questionid
    *   The questionid property used to update the correct question.
    * @param {string} question
    *   The question property used to update the question.
    * @param {integer} answer
    *   The answer property used to update the question.
    * @param {string} distractors
    *   The distractors property used to update the question.
    */
    
    $scope.updateQuestion = function(questionid, question, answer, distractors){
        
        for(i = 0; i < globalList.length ; i++){
            if (globalList[i].questionid == questionid) {
                globalList[i].question = question
                globalList[i].answer = answer
                globalList[i].distractors = distractors
            }
        }
        
        $scope.displayTable(currentPage)
    }
    
    
   /**
    * 
    *   Returns a list of json objects from a response
    *
    * @param {response} response
    *   The response object that contains the questions
    *   recieved from the server.
    * 
    * @param {array} 
    *   The array of json objects
    *
    */
    
    $scope.convertResponseToJson = function(response){
        
        jsonArray = []
        
        for(i = 0; i < response.data.list.length; i++){
            jsonArray.push(JSON.parse(response.data.list[i]))
        }
        
        return jsonArray    
    }
    
    
    //  Initializes the questions page.
    $scope.init()
    
});
  
