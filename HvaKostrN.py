from DbaKahootQuizMaker import *
import sys
from uploadimagesToKahoot import *
import argparse

# named command line arguments
parser=argparse.ArgumentParser()
parser.add_argument("--amount", help="amount of questions below 35")
parser.add_argument("--name", help="name of the quiz")
parser.add_argument("--openbrowser", help="whether to open a window with the quiz or not, default false")

args=parser.parse_args()


def createAndUploadQuiz(amount = "", quizName = None, openbrowser = False):
    """Creates and uploads quiz to Kahoot, Remember to configure auth.Json"""
    if amount == None:
        amount = ""
    exportFolder = ""
    if quizName == None:
        exportFolder = CreateQuiz(amount)
    else: 
        exportFolder = CreateQuiz(amount, quizName)
    upload_quiz_to_kahoot(exportFolder, openbrowser)
    return

if __name__== "__main__":
    createAndUploadQuiz(args.amount, args.name, args.openbrowser)
    
