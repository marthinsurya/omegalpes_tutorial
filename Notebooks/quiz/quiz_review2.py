import ipywidgets as widgets
import sys
from IPython.display import display, HTML
from IPython.display import clear_output

out = widgets.Output()


alternativ = widgets.RadioButtons(
    options=[('Grid Import', 1), ('Total consumption', 2),('Energy surplus/Grid Export',3)],
    description='',
    disabled=False
)
print('\033[1m','What changes you observe from the result graph?','\033[0m')
check = widgets.Button(description="Review")
display(alternativ)
display(check)


def choice(b):
    a = int(alternativ.value)
    first_answer = 1
    second_answer = 2


    if(a==first_answer):
        print( "You are right! Import has become less due to battery discharge.")


    elif(a==second_answer):
        print("Total consumption doesn't change, but part of it (washing machine) is moved to a more optimized operation time")


    else:
         print("You are right! Do you realize that the grid export is actually 0 now? Energy surplus is optimized considering all of variables.\n"
               "Resulting in battery and washing machine sharing the energy surplus.")


display(out)
check.on_click(choice)

with out:
    out.clear_output()
