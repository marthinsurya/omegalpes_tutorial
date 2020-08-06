#from quizs.question import Question
import ipywidgets

class Question:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer

question_prompts =[
    "How much energy was imported from the grid?\n",
    "How much energy was consumed from the PV?\n",
    "How many energy units are there in the energy system?\n"
]

questions =[
    Question(question_prompts[0], str(1)),
    Question(question_prompts[1], str(2)),
    Question(question_prompts[2], str(3))
]

def run_test(questions):
    score=0

    for question in questions:
        answer=input(question.prompt)
        if answer == question.answer:
            score +=1


    if score ==len(question_prompts):
        print("you got " + str(score) + " / " + str(
                     len(questions)) + "correct, your key to further your journey %run quiz2")
    else:
        print(
             "you got " + str(score) + " / " + str(len(questions)) + "correct, you need to complete to progress further")
        print('\033[1;31;1m', 'Are you ready to redo again?', '\033[1;31;0m')
        run_test(questions)
        #retake = ipywidgets.Button(description="retake")
        #display(retake)

        #def redo():
        #    run_test(questions)

        #retake.on_click(redo)




run_test(questions)
