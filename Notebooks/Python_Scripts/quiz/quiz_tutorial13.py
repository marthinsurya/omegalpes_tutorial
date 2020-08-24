import ipywidgets as widgets
import sys
from IPython.display import display, HTML
from IPython.display import clear_output

out = widgets.Output()


alternativ = widgets.RadioButtons(
    options=[('3', 1), ('14', 2),('17',3)],
    description='',
    disabled=False
)
print('\033[1m','Did you realize that the model was optimized according to the objective grid_import.minimize_production?\n'
                'OmegAlpes will prioritize PV production before importing electricity from the grid. Do you know at what hour it happened?','\033[0m')
check = widgets.Button(description="check answer")
display(alternativ)
display(check)


def choice(b):
    a = int(alternativ.value)
    first_answer = 1
    second_answer = 2


    if(a==first_answer):
        print( "Incorrect, in this period John imports electricty since there is no PV production")


    elif(a==second_answer):
        print("Incorrect, in this period John exports electricity to the grid since there is surplus after consumption")


    else:
         print("You are right! John doesn't have enough PV production so he has to import fron the grid. Here is your last magic word 'BROCOLLI'!")


display(out)
check.on_click(choice)

with out:
    out.clear_output()
