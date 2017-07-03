#!/usr/bin/env python
#title           : Constants.py
#description     : A module with hardcoded string 
#                : literals used to access properties
#                : in the database.
#author          : Daniel Ribeirinha-Braga
#date            : 7/2/2017
#==============================================================================


# The table name of the database
QUESTION_TABLE = 'Question'

# The table properties used to access
# the question properties
QUESTION_ID = 'questionid'
QUESTION = 'question'
ANSWER = 'answer'
DISTRACTORS = 'distractors'

# Operaters used in database calls
GREATER = '>'
LESS = '<'
EQUAL = '='

# Operaters strings used in database calls
GREATERSTRING = 'GREATER'
LESSSTRING = 'LESS'
EQUALSTRING = 'EQUAL'


if __name__ == '__main__':
    print('Printing all constants')
    print()
    print('Printing Tables used:')
    print(QUESTION_TABLE)
    print()
    print('Printing columns:')
    print(QUESTION_ID)
    print(QUESTION)
    print(ANSWER)
    print(DISTRACTORS)
    print()
    print('Printing operators that are used:')
    print(GREATER)
    print(LESS)
    print(EQUAL)
    
