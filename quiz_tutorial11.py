import ipywidgets as widgets
import sys
from IPython.display import display, HTML
from IPython.display import clear_output

out = widgets.Output()


alternativ = widgets.RadioButtons(
    options=[('TimeUnit', 1), ('FixedConsumptionUnit', 2), ('FixedProductionUnit', 3),('VariableConsumptionUnit',4)],
    description='',
    disabled=False
)
print('\033[1m','If we have pv production profile data, what can we use it for?','\033[0m')
check = widgets.Button(description="check answer")
display(alternativ)
display(check)


def choice(b):
    a = int(alternativ.value)
    first_answer = 1
    second_answer = 2
    third_answer= 3

    if(a==first_answer):
        print( "Incorrect! TimeUnit is used to define the studied time period with defined timestep.")


    elif(a==second_answer):
        print("Incorrect! FixedConsumptionUnit is used to create consumption unit with fixed load profile.")


    elif(a==third_answer):
        print("You are right! FixedProductionUnit is used to create production unit with fixed production profile. Magic word no.1 is 'JANE'")

    else:
         print("Incorrect! VariableConsumptionUnit is used to create consumption unit for non-fixed consumption profile.")


display(out)
check.on_click(choice)

with out:
    out.clear_output()
