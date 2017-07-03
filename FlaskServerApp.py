#!/usr/bin/env python
#title           : FlaskServerApp.py
#description     : My main Flask Server Application that
#                : takes in a input.csv with question information
#                : and constructs a database, endpoints, and website
#                : in order for the user to manipulate it on host ip
#                : http://127.0.0.1:5000.
#author          : Daniel Ribeirinha-Braga
#date            : 7/2/2017
#==============================================================================
from flask import Flask, request, jsonify, json, render_template, make_response
from QuestionObject import Question
from DBM import DBManager

import sys, os, Constants
     

# Iniializing the Flask application and setting 
# properties.
app = Flask(__name__, static_url_path='')
dbm = None
htmlDefault = 'index.html'
OKCode = 200
BadCode = 400
OKText = 'OK'
BadText = 'Bad Request'


""" Routs the user to the main page
    of the application when user
    goes to http://127.0.0.1:5000.
    @return  {Page}
        The html page being rendered on the server.
    """
    
@app.route('/')
def getMainPage():
    return render_template('index.html')

    
""" Endpoint for getting all of the 
    questions in the questions table.
    @return  {response}
        A response from the server attempting
        to get all the questions from the 
        questions table.
    """
    
@app.route('/getquestions', methods=['GET'])
def getQuesions():

    questions = dbm.getQuestions()
    
    if questions is None:
        questions = []
        text = BadText
        code = BadCode
        success = False
    else:
        text = OKText
        code = OKCode
        success = True
        
    questionsJson = convertToResponse(questions,text,code,success)
    
    return questionsJson

    
""" Endpoint for getting a specific
    question based on the questionid.
    @return  {response}
        A response from the server attempting
        to get a specific question from the 
        questions table.
    """
    
@app.route('/getquestion', methods=['GET'])
def getQuesion():
    
    qid = request.args.get('questionid')
    requestValid = paramsValid(qid,None,None,None)
    
    if requestValid:
        questions = dbm.getQuestion(qid)
    else:
        questions = None
    
    if questions is None:
        questions = []
        text = BadText
        code = BadCode
        success = False
    elif len(questions) == 1:
        text = OKText
        code = OKCode
        success = True
    elif len(questions) == 0 :
        text = 'No Question with current id: ' + str(qid)
        code = OKCode
        success = True
    
    questionsJson = convertToResponse(questions,text,code,success)
    
    return questionsJson
    
    
""" Endpoint for deleting a specific
    question based on the questionid.
    @return  {response}
        A response from the server attempting
        to delete a specific question from the 
        questions table.
    """
   
@app.route('/deletequestion', methods=['DELETE'])
def deleteQuestion():

    qid = request.args.get('questionid')
    requestValid = paramsValid(qid,None,None,None)
    
    if requestValid:
        deleted = dbm.deleteQuestion(qid)
    else:
        deleted = None
        
    questions = []
    
    if deleted is None:
        text = BadText
        code = BadCode
        success = False
    else:
        text = OKText
        code = OKCode
        success = True
        deletedQ = Question([qid,None,None,None])
        questions.append(deletedQ)

    questionsJson = convertToResponse(questions,text,code,success)
    
    return questionsJson
        
        
""" Endpoint for inserting a new
    question based on the question
    parameters provided in the request.
    @return  {response}
        A response from the server attempting
        to insert a new question into the 
        questions table.
    """
    
@app.route('/insertquestion', methods=['POST'])
def insertQuestions():
    
    question = request.args.get('question')
    answer = request.args.get('answer')
    distractors = request.args.get('distractors')
    requestValid = paramsValid(None,question,answer,distractors)
    
    if requestValid:
        qid = dbm.insertQuestion(question,answer,distractors)
    else:
        qid = None
    
    questions = []
    
    if qid is None:
        text = BadText
        code = BadCode
        success = False
    else:
        text = OKText
        code = OKCode
        success = True
        newQ = Question([qid,question,answer,distractors])
        questions.append(newQ)
    
    questionsJson = convertToResponse(questions,text,code,success)
    
    return questionsJson
    
    
""" Endpoint for updating anew
    question based on the question
    parameters provided.
    @return  {response}
        A response from the server attempting
        to update a question in the 
        questions table.
    """
    
    
@app.route('/updatequestion', methods=['POST'])
def updateQuestion():

    qid = request.args.get('questionid')
    question = request.args.get('question')
    answer = request.args.get('answer')
    distractors = request.args.get('distractors')
    requestValid = paramsValid(qid,question,answer,distractors)
    
    if requestValid:
        updated = dbm.updateQuestion(qid,question,answer,distractors)
    else:
        updated = None
    
    questions = []
    
    if updated is None:
        text = BadText
        code = BadCode
        success = False
    else:
        text = OKText
        code = OKCode
        success = updated
        newQ = Question([qid,question,answer,distractors])
        questions.append(newQ)

    questionsJson = convertToResponse(questions,text,code,success)
    
    return questionsJson

    
""" Endpoint for retrieving all of
    the questions that have similar 
    character sequence in the question 
    property to the one provided that are
    privoded by the request.
    @return  {response}
        A response from the server attempting
        to get all the questions that have 
        a similar character sequence in the
        question property.
    """
    
@app.route('/getquestionsfromquestion', methods=['GET'])
def getQuesionFromQuestion():

    question = request.args.get('question')
    requestValid = paramsValid(None,question,None,None)
    
    if requestValid:
        questions = dbm.getQuestionsWhereQuestion(str(question))
    else:
        question = None
    
    if questions is None:
        questions = []
        text = BadText
        code = BadCode
        success = False
    else:
        text = OKText
        code = OKCode
        success = True
        
    questionsJson = convertToResponse(questions,text,code,success)

    return questionsJson
    
""" Endpoint for retrieving all of
    the questions that meet a condition
    with the answer property.
    @return  {response}
        A response from the server attempting
        to get all of the questions that meet
        the critiera for the answer.
    """
    
@app.route('/getquestionsfromanswer', methods=['GET'])
def getQuesionFromAnswer():

    answer = request.args.get('answer')
    condition = request.args.get('condition')
    
    requestValid = (paramsValid(None,None,answer,None) and 
        (condition == Constants.EQUALSTRING or condition == Constants.LESSSTRING or
        condition == Constants.GREATERSTRING))
    
    if requestValid:
        questions = dbm.getQuestionsWhereAnswer(condition,answer)
    else:
        questions = None
    
    if questions is None:
        questions = []
        text = BadText
        code = BadCode
        success = False
    else:
        text = OKText
        code = OKCode
        success = True
        
    questionsJson = convertToResponse(questions,text,code,success)

    return questionsJson
    
""" Endpoint for retrieving all of
    the questions that have similar 
    character sequence in the distractors
    property to the one provided that are
    privoded by the request.
    @return  {response}
        A response from the server attempting
        to get all the questions that have 
        a similar character sequence in the
        distractor property.
    """

@app.route('/getquestionsfromdistractors', methods=['GET'])
def getQuesionFromDistractors():

    distractors = request.args.get('distractors')
    requestValid = paramsValid(None,None,None,distractors)
    
    if requestValid:
        questions = dbm.getQuestionsWhereDistractors(distractors)
    else:
        questions = None
    
    if questions is None:
        questions = []
        text = BadText
        code = BadCode
        success = False
    else:
        text = OKText
        code = OKCode
        success = True
        
    questionsJson = convertToResponse(questions,text,code,success)
        
    return questionsJson
    
############################################################   
# Following endpoints are not used because created better
# implementation above.   

""" Endpoint for updating the answer property 
    of a question.
    @param {integer} qid
        The questionid to identify what
        question to update.
    @param {integer} answer
        The new answer property to set.
    @return  {response}
        A response from the server attempting
        to update the answer property.
    """

   
@app.route('/updateanswer/<int:qid>/<int:answer>', methods=['POST'])
def updateAnswer(qid,answer):
    
    updated = dbm.updateAnswer(qid,answer)
    questions = []
    
    if updated is None:
        text = BadText
        code = BadCode
        success = False
    else:
        text = OKText
        code = OKCode
        success = updated

    questionsJson = convertToResponse(questions,text,code,success)
    
    return questionsJson
    
""" Endpoint for updating the distractor property 
    of a question.
    @param {integer} qid
        The questionid to identify what
        question to update.
    @param {integer} distractors
        The new distractors property to set.
    @return  {response}
        A response from the server attempting
        to update the answer property.
    """
    
@app.route('/updatedistractors/<int:qid>/<string:distractors>', methods=['POST'])
def updateDistractors(qid,distractors):
    
    updated = dbm.updateDistractor(qid,distractors)
    questions = []
    
    if updated is None:
        text = BadText
        code = BadCode
        success = False
    else:
        text = OKText
        code = OKCode
        success = updated

    questionsJson = convertToResponse(questions,text,code,success)
    
    return questionsJson

############################################################    
    
    
""" Takes in four properties of a http response
    and creates an appropriate response object to 
    return to the client.
    @param {Array} array
        The array of question json objects to
        return to the client.
    @param {string} text
        The text to put into the response message.
    @param {integer} code
        The code of the response from the server.
    @param {boolean} success
        The property that indicates if request was
        successful or not.
    @return  {response}
        A response to provide to the client.
    """
    
def convertToResponse(array,text,code,success):
    
    myArray = []
    for question in array:
        myArray.append(json.dumps(question.__dict__))
    
    jsonObject = jsonify(list=myArray,text=text,code=code,success=success)
    response = make_response(jsonObject)
    response.headers.set('Content-Type','application/json')
    
    return response
    
    
""" Checks if the params from the request are valid.
    @param {string} questionid
        The questionid property to check and see if it is valid.
    @param {string} question
         The question property to check and see if it is valid.
    @param {string} answer
        The answer property to check and see if it is valid.
    @param {string} distractors
        The distractor property to check and see if it is valid.
    @return  {Boolean}
        True if parameters from the request are valid,
        false otherwise.
    """
 
    
def paramsValid(questionid,question,answer,distractors):
    
    if questionid:
        if not isinstance(int(questionid),int):
            return False
            
    if question:
        if not isinstance(question,str):
            return False
         
    if answer:
        if not isinstance(int(answer),int):
            return False
            
    if distractors:
        if not isinstance(distractors,str):
            return False
            
    return True
    
# The AngularJS/Flask Application Main Method
if __name__ == "__main__":
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            dbm = DBManager('pluralsight.db')
            dbm.createTable(sys.argv[1])
            app.run()
        else: 
            print("File does not exist")
            sys.exit()   
    else:
        print("No file provided")
        sys.exit()
        

        

