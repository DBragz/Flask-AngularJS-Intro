#!/usr/bin/env python
#title           : DBM.py
#description     : A database management system used
#                : in order to get question information
#                : out of the database.
#author          : Daniel Ribeirinha-Braga
#date            : 7/2/2017
#==============================================================================

import sqlite3, csv, sys, os, Constants
from QuestionObject import Question

class DBManager:
    
    """ Constructor for the database 
        management object.
        @param {string} name
            The name of the database if given.
        """
    
    def __init__(self, name):
        
        self.name = name
        if name is not None:
            self.createDB(self.name)
    
    
    """ Creates the database with the 
        param provided.
        @param {string} name
            The name of the database.
        """
    
    def createDB(self, name):
    
        if not os.path.isfile(name):
            self.name = name
            try:
                con = sqlite3.connect(name)
                print('Database Created')
            except :
                print('Error: Unable to create database')
                sys.exit()
            finally:
                if con:
                    con.close()
            
        else:
            print('Database Already Exists')
    
    
    """ Parse the given file containing question 
        information and create a question table.
        param provided.
        @param {string} file
            The name of the file to use to create
            the database.
        """
    
    def createTable(self, file):

        try:
            with open(file,'rU') as csvfile:
                dr = csv.DictReader(csvfile, delimiter='|')
                to_db = []
                for i in dr:
                    distractors = i[Constants.DISTRACTORS].replace(' ','')
                    to_db.append((i[Constants.QUESTION], i[Constants.ANSWER], distractors))
                
            con = sqlite3.connect(self.name)
            cur = con.cursor()   
            
            cur.execute('DROP TABLE IF EXISTS ' + Constants.QUESTION_TABLE)
            cur.execute('''CREATE TABLE ''' + Constants.QUESTION_TABLE +  ''' (''' + Constants.QUESTION_ID + ''' INTEGER PRIMARY KEY,''' + 
                            Constants.QUESTION + ''' varchar(20) NOT NULL,''' +  
                            Constants.ANSWER + ''' integer NOT NULL,''' + 
                            Constants.DISTRACTORS + ''' avarchar(20) NOT NULL);''')
            cur.executemany('INSERT INTO '  + Constants.QUESTION_TABLE + ' (' + Constants.QUESTION + ', ' + Constants.ANSWER + ', ' + Constants.DISTRACTORS + ' ) VALUES (?, ?, ?);', to_db)
            
            for row in cur.execute('SELECT * FROM ' + Constants.QUESTION_TABLE):
                print(row)
            
            con.commit()
            con.close()
            
        except (OSError, IOError, lite.Error) as e:
            print('Error: Unable to create database')
            sys.exit()
        finally:
            if con:
                con.close()
        
        
    """ Creates the database with the 
        param provided.
        @param {integer} questionid
            The question id to retrieve from the
            database.
        @return {Question} A question object from the database.
        """
    
    def getQuestion(self, questionid):
    
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        cur.execute('SELECT * FROM ' + Constants.QUESTION_TABLE + ' where ' + Constants.QUESTION_ID + ' ' 
        + Constants.EQUAL + ' ' + str(questionid))
        data = cur.fetchall()
        con.close()
        
        return self.convertToObject(data)
        
        
    """ Gets all the questions currently 
        in the database.
        @return {Array} All of the Question objects  
                in the database.
        """
        
    def getQuestions(self):
    
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        cur.execute('SELECT * FROM ' + Constants.QUESTION_TABLE)
        data = cur.fetchall()
        con.close()
        
        return self.convertToObject(data)

        
    """ Gets all the questions currently 
        in the database that meet a specific
        condition with the answer property.
        @param {string} condition
            The string litterally to identify what
            operator to use in the comparison query.
        @param {integer} value
            The integer value to use in the comparison.
        @return {Array} All of the Question objects  
                in the database that meet query condition.
        """
        
    def getQuestionsWhereAnswer(self, condition, value):
    
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        
        if(condition == Constants.GREATERSTRING):
            cur.execute('SELECT * FROM ' + Constants.QUESTION_TABLE + ' WHERE ' + Constants.ANSWER 
            + ' ' + Constants.GREATER + ' ' + str(value))
        elif(condition == Constants.LESSSTRING):
            cur.execute('SELECT * FROM ' + Constants.QUESTION_TABLE + ' WHERE ' + Constants.ANSWER 
            + ' ' + Constants.LESS + ' ' + str(value))
        elif(condition == Constants.EQUALSTRING):
            cur.execute('SELECT * FROM ' + Constants.QUESTION_TABLE + ' WHERE ' + Constants.ANSWER 
            + ' ' + Constants.EQUAL + ' ' + str(value))
        else:
            print('No condition supplied')
        
        
        data = cur.fetchall()
        con.close()
        
        return self.convertToObject(data)
    
    
    """ Gets all the questions where the question 
        property in the database that have similar 
        characters to the string literal.
        @param {string} string
            The string litteral to compare to 
            the question property in the database.
        @return {Array} All of the Question objects  
                in the database that similar characters
                as the one in the string literal.
        """
    
    def getQuestionsWhereQuestion(self, string):
    
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        cur.execute('SELECT * FROM ' + Constants.QUESTION_TABLE + ' WHERE ' + Constants.QUESTION + " LIKE '%" + string + "%'")
        data = cur.fetchall()
        con.close()
        
        return self.convertToObject(data)
    
    
    """ Gets all the questions where the distractors 
        property in the database that have similar 
        characters to the string literal.
        @param {string} string
            The string litteral to compare to 
            the distractors property in the database.
        @return {Array} All of the Question objects  
                in the database that similar characters
                as the one in the string literal.
        """
    
    def getQuestionsWhereDistractors(self, string):
    
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        cur.execute('SELECT * FROM ' + Constants.QUESTION_TABLE + ' WHERE ' + Constants.DISTRACTORS + " LIKE '%" + string + "%'")
        data = cur.fetchall()
        con.close()
        
        return self.convertToObject(data)
    
    
    """ Takes question properties and adds a 
        new question to the table. It then
        returns the rowid given to send back 
        to the frontend.
        @param {string} question
            The string litteral to use as the 
            question property for the new question.
        @param {integer} answer
            The integer to use as the 
            answer property for the new question.
        @param {string} distractors
            The string litteral to use as the 
            distractors property for the new question.
        @return {integer} The new id for the question that was 
                succesfully inserted into the table.
        """
    
    def insertQuestion(self, question, answer, distractors):
    
        insertedQuestion = False
    
        try: 
            con = sqlite3.connect(self.name)
            cur = con.cursor()
            val = cur.execute('INSERT INTO ' + Constants.QUESTION_TABLE + ' (' + Constants.QUESTION + ', ' + Constants.ANSWER + ', ' + 
                Constants.DISTRACTORS + ') VALUES (?, ?, ?);', (question,answer,distractors)).rowcount
            qid = cur.lastrowid
            con.commit()
            
            if val and qid:
                insertStatus = True
            else:
                qid = None
                
        except:
            con.rollback()
            insertStatus = False
        finally:
            con.close()
        
        
        return qid
        
        
    """ Deletes a question in the database 
        with the given questionid.
        @param {integer} questionid
            The questionid to delete from the
            question table.
        @return The new id for the question that was 
                succesfully inserted into the table.
        """
        
    def deleteQuestion(self, questionid):
        
        deletedStatus = False
        
        try:
            con = sqlite3.connect(self.name)
            cur = con.cursor()
            val = cur.execute('DELETE FROM ' + Constants.QUESTION_TABLE + ' WHERE ' + Constants.QUESTION_ID + ' ' 
                + Constants.EQUAL + ' ' + str(questionid)).rowcount
            con.commit()
            
            if val:
                deletedStatus = True
                
        except Error:
            con.rollback()
            deletedStatus = False
        finally:
            con.close()
        
        if deletedStatus:
            return questionid
        else:
            return None
        
        
    """ Updates a question with the new 
        properties provided in the method.        
        @param {integer} questionid
            The questionid to delete from the
            question table.
        @param {string} question
            The string litteral to use as the 
            question property for the updated question.
        @param {integer} answer
            The integer to use as the 
            answer property for the updated question.
        @param {string} distractors
            The string litteral to use as the 
            distractors property for the updated question.
        @return {Boolean} True if successfully updated,
                    False otherwise.
        """
        
    def updateQuestion(self, questionid, question, answer, distractors):
        
        updateStatus = False
        
        try:
            con = sqlite3.connect(self.name)
            cur = con.cursor()
            val = cur.execute('UPDATE ' + Constants.QUESTION_TABLE + ' SET ' + Constants.QUESTION + ' ' + Constants.EQUAL  + " '" + str(question) + 
                ', ' + Constants.ANSWER + ' ' + Constants.EQUAL + ' ' + answer + ', ' + Constants.DISTRACTORS + ' ' +
                Constants.EQUAL + ' ' + distractors + 
                "' WHERE " + Constants.QUESTION_ID + ' ' + Constants.EQUAL + ' ' + str(questionid)).rowcount
            con.commit()
            if val:
                updateStatus= True
                
        except:
            con.rollback()
            updateStatus = False
        finally:
            con.close()
    
        return updateStatus
    
    """ Used to take the database querys values,
        the Array of questions, and convert 
        them all to question objects.
        @param {Array} array
            The array of questions as an array structure.
        @return {Array} True if successfully updated,
                    False otherwise.
        """
    
    def convertToObject(self, array):
        myArray = []
        for row in array:
            myArray.append(Question(row))
        
        return myArray
    
    
    # These are initial functions that I started to implement 
    # and they work however I don't use them due to better 
    # implementation above.
    
    """ Method used to update an answer.
        @param {integer} questionid
            The questionid used to identify 
            what question in table.
        @param {integer} value
            The new answer property of a question.
        @return {Boolean} True if successfully updated,
                    False otherwise.
        """
    
    def updateAnswer(self, questionid, value):
       
        updateStatus = False
       
        try:
            con = sqlite3.connect(self.name)
            cur = con.cursor()
            val = cur.execute('UPDATE ' + Constants.QUESTION_TABLE + ' SET ' + Constants.ANSWER + 
                ' = ' + str(value) + ' WHERE ' + Constants.QUESTION_ID + ' ' + Constants.EQUAL + ' ' + str(questionid)).rowcount
            con.commit()
          
            if val:            
                updateStatus = True
                
        except:
            con.rollback()
            updateStatus = False
        finally:
            con.close()
            
        return updateStatus
    
    """ Method used to update a distractor.
        @param {integer} questionid
            The questionid used to identify 
            what question in table.
        @param {string} string
            The new distractor property of a question.
        @return {Boolean} True if successfully updated,
                    False otherwise.
        """
    
    
    def updateDistractor(self, questionid, string):
        
        updateStatus = False
        
        try:
        
            con = sqlite3.connect(self.name)
            cur = con.cursor()
            val = cur.execute('UPDATE ' + Constants.QUESTION_TABLE + ' SET ' + Constants.DISTRACTORS + " = '" 
            + string + "' WHERE " + Constants.QUESTION_ID + ' ' + Constants.EQUAL + ' ' + str(questionid)).rowcount
            con.commit()
            
            if val:
                updateStatus = True
                
        except:
            con.rollback()
            updateStatus = False
        finally:
            con.close()
        
        return updateStatus
    
    """ Prints the rows of the DBM's
        current table in the database.
        """
    
    def printData():
    
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM ' + Constants.QUESTION_TABLE):
            print(row)
        con.commit()
        con.close()
    
    """ Method used to update a specific propety 
        of a question given the questionid.
        @param {integer} questionid
            The questionid used to update.
        @param {string} column
            The question property to update.
        @param {string} value
            The new value of the column selected.
        """
    
    def updateData(self, questionid, column, value):
        
       con = sqlite3.connect(self.name)
       cur = con.cursor()
       cur.execute('UPDATE question_table SET ' + str(column) + ' = ' + str(value) + ' WHERE questionid = ' + str(questionid))
       con.commit()
       con.close()
    
       print('Updating question with id ' + str(questionid) + ' column ' + str(column) + ' value ' + str(value))
            
    
        
   
        
        
    
    