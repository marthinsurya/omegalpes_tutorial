##basic text input quiz
from ipywidgets import widgets, Layout, Box, GridspecLayout


def create_textinputquiz_widget(description, text_description, correct_answer, a2, hint):  ##grid for option table

    correct_answer = correct_answer  ##float ##str
    alternativ = widgets.Text(value='',
                              placeholder='',
                              description='',
                              disabled=False, layout=(Layout(width='auto'))
                              )
    ##question description
    description_out = widgets.Output(layout=Layout(width='auto'))
    with description_out:
        print(description)
    ##description before text widget
    text_description_out = widgets.Output(layout=Layout(width='auto'))
    with text_description_out:
        print(text_description)
    ##description after text widget e.g. units
    a2_out = widgets.Output(layout=Layout(width='auto'))
    with a2_out:
        print(a2)
    ##
    feedback_out = widgets.Output()

    def check_selection(b):
        a = alternativ.value

        if a == correct_answer:
            s = "Correct!"

        else:
            s = "Wrong answer unfortunately"
        with feedback_out:
            feedback_out.clear_output()
            print(s)

        return

    check = widgets.Button(description="check")
    check.on_click(check_selection)
    ##
    hint_out = widgets.Output()

    def hint_selection(b):
        with hint_out:
            print(hint)
        with feedback_out:
            feedback_out.clear_output()
            print(hint)

    hintbutton = widgets.Button(description="hint")
    hintbutton.on_click(hint_selection)

    return widgets.VBox([description_out,
                         widgets.HBox([text_description_out, alternativ, a2_out]),
                         widgets.HBox([hintbutton, check]), feedback_out],
                        layout=Layout(display='flex',
                                      flex_flow='column',
                                      align_items='stretch',
                                      width='auto'))



def quiz():
    questions1 = create_textinputquiz_widget('What is the value of dt if you have 5 minutes timestep data?', "answer:", '1/12', "hour",
                                            '[hint]: Read part 1.1')
    questions2 = create_textinputquiz_widget('Is the timeunit same for all energy units?', "answer:", 'yes', "!",
                                             '[hint]: Read part 1.6')
    questions3 = create_textinputquiz_widget('How many production units we have in this model with energy flow always out?', "answer:", '2', "unit(s)",
                                             '[hint]: Read part 1.3')
    questions4 = create_textinputquiz_widget('How many consumption units we have in this model with energy flow always in?', "answer:", '3',
                                             "unit(s)", '[hint]: Read part 1.3')
    questions5 = create_textinputquiz_widget('Is energy flow of storage always in?', "answer:",
                                             'no', "!",'[hint]: Read part 1.3.1')
    questions6 = create_textinputquiz_widget('How much electricity was exported?', "answer:",
                                             '0', "kWh", '[hint]: Read part 1.5')
    questions7 = create_textinputquiz_widget('At what hour the storage was discharged?', "answer:",
                                             '20', "hour", '[hint]: Read part 1.8')
    questions8 = create_textinputquiz_widget('How much electricity was imported this time? (one decimal)', "answer:",
                                             '4.7', "kWh", '[hint]: Read part 1.8')
    display(questions1)
    display(questions2)
    display(questions3)
    display(questions4)
    display(questions5)
    display(questions6)
    display(questions7)
    display(questions8)


quiz()