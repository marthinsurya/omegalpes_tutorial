import ipywidgets as widgets
import sys
from IPython.display import display, HTML
from IPython.display import clear_output

out = widgets.Output()


alternativ = widgets.RadioButtons(
    options=[('grid_import.minimize_operating_cost()', 1), ('grid_production_a.minimize_operating_cost()', 2),('grid_production_b.minimize_operating_cost()', 3)],
    description='',
    disabled=False
)
print('\033[1m','How to write the line to define objective to minimize operating cost?','\033[0m')
check = widgets.Button(description="check answer")
display(alternativ)
display(check)


def choice(b):
    a = int(alternativ.value)
    first_answer = 1
    sec_ans=2

    if(a==first_answer):
        print( "Incorrect, remember we haven't defined grid_import. Instead, we defined each grid import as grid_production_a and grid_production_b")

    elif (a==sec_ans):
        print("You are right! but John is not importing from Grid A alone.")
    else :
        print("You are right again! We want to minimize grid import so we should include both in the objectives. \n'"
              "Write these 2 lines in below box and here is the fourth level 2 magic word 'CRUSH'!")


display(out)
check.on_click(choice)

with out:
    out.clear_output()
