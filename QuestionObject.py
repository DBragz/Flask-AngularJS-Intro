#!/usr/bin/env python
#title           : QuestionObject.py
#description     : A Question object used to manipulate the
#                : database and website information.
#author          : Daniel Ribeirinha-Braga
#date            : 7/2/2017
#==============================================================================



class Question:

    """ Constructor for the Question object.
        """
        
    def __init__(self, array):
        self.questionid = array[0]
        self.question = array[1]
        self.answer = array[2]
        
        if array[3] is not None:
            self.distractors = array[3].split(',')
        else:
            self.distractors = None