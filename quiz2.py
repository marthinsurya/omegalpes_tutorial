import ipywidgets as widgets
import sys
from IPython.display import display, HTML
from IPython.display import clear_output

#from ipython.display import clear_output

out = widgets.Output()


alternativ = widgets.RadioButtons(
    options=[('battery link with description', 1), ('grid price comparison link with description', 2), ('heat source link with description', 3)],
    description='',
    disabled=False
)
print('\033[1m','What path do you want to choose?','\033[0m')
check = widgets.Button(description="Proceed")
display(alternativ)
display(check)


def choice(b):
    a = int(alternativ.value)
    firstanswer = 1
    secanswer = 2

    if(a==firstanswer):
        #color = '\x1b[6;30;42m' + "Riktig." + '\x1b[0m' +"\n" #green color


        # create a string template for the HTML snippet
        link_t = "<a href='./tutorial 1.ipynb' target='_blank'> Click here to start simulating battery with Omegalpes</a>"


        # create HTML object, using the string template
        html = HTML(link_t.format())

                # display the HTML object to put the link on the page:
        display(html)

    elif(a==secanswer):
        link_t = "<a href='./tutorial 1.ipynb' target='_blank'> Click here to start comparing grid prices with Omegalpes</a>"

        # create HTML object, using the string template
        html = HTML(link_t.format())

        # display the HTML object to put the link on the page:
        display(html)

    else:

        link_t = "<a href='./tutorial 1.ipynb' target='_blank'> Click here to start simulating heat conversion with Omegalpes</a>"

# create HTML object, using the string template
        html = HTML(link_t.format())

# display the HTML object to put the link on the page:
        display(html)

    svar = ["","","",""]
    with out:
        clear_output()
    #with out:
    #print(color+""+svar[a-1])



display(out)
check.on_click(choice)