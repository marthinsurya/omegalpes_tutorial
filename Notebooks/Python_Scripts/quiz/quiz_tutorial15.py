#from quizs.question import Question
import ipywidgets

class Question:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer

question_prompts =[
    "Timestep in this simulation is ___ hour(s)\n",
    "The period of study is ____ hour(s)\n",
    "How many energy units are there in the model we created?\n",
    "How many fixed energy units we have in the model we created?\n",
    "How many variable energy units we have in the model we created?\n",
    "How many nodes we have in this model we created?\n",
    "How many objectives we have in this model we created?\n",
    "Is there any energy export in this simulation?\n",
    "Is there any energy import in this simulation?\n",
    "How many instances the export occur in this simulation?\n",
    "Does pv production cover the consumption outside its period of production?\n",
    "Is there any import during pv production period?"
]

questions =[
    Question(question_prompts[0], str(1)),
    Question(question_prompts[1], str(24)),
    Question(question_prompts[2], str(4)),
    Question(question_prompts[3], str(2)),
    Question(question_prompts[4], str(2)),
    Question(question_prompts[5], str(1)),
    Question(question_prompts[6], str(1)),
    Question(question_prompts[7], 'yes'),
    Question(question_prompts[8], 'yes'),
    Question(question_prompts[9], str(4)),
    Question(question_prompts[10], 'no'),
    Question(question_prompts[11], 'yes')
]

def run_test(questions):
    score=0

    for question in questions:
        answer=input(question.prompt)
        if answer == question.answer:
            score +=1


    if score ==len(question_prompts):
        print("Great! You got " + str(score) + " / " + str(
                     len(questions)) + "correct. You have cleared Tutorial 1.")
    else:
        print(
             "You got " + str(score) + " / " + str(len(questions)) + "correct, try to get full points !!")
        print('\033[1;31;1m', 'Are you ready to redo again?', '\033[1;31;0m')
        run_test(questions)

run_test(questions)
