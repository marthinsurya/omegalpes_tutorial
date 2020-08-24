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
    questions1 = create_textinputquiz_widget('What is the timestep in this model?', "answer:", '1', "hour(s)",
                                            '[hint]: Read part 1.1')
    questions2 = create_textinputquiz_widget('What is the study period in this model?', "answer:", '24', "hour(s)",
                                             '[hint]: Read part 1.1')
    questions3 = create_textinputquiz_widget('How many energy units are there in this model?', "answer:", '4', "unit(s)",
                                             '[hint]: Read part 1.3')
    questions4 = create_textinputquiz_widget('How many fixed energy units we have in this model?', "answer:", '2',
                                             "unit(s)", '[hint]: Read part 1.3.1')
    questions5 = create_textinputquiz_widget('How many variable energy units we have in this model?', "answer:",
                                             '2', "unit(s)",'[hint]: Read part 1.3.1')
    questions7 = create_textinputquiz_widget('How many nodes we have in this model?', "answer:",
                                             '1', "node(s)", '[hint]: Read part 1.6')
    questions6 = create_textinputquiz_widget('How many objectives we have in this model', "answer:",
                                             '1', "objective(s)", '[hint]: Read part 1.5')
    questions8 = create_textinputquiz_widget('Is there any energy export in this simulation?', "answer:",
                                             'yes', "!", '[hint]: Read part 1.10')
    questions9 = create_textinputquiz_widget('Is there any energy import in this simulation?', "answer:",
                                             'yes', "!", '[hint]: Read part 1.10')
    questions10 = create_textinputquiz_widget('How many instances the export occur in this simulation?', "answer:",
                                             '4', "instance(s)", '[hint]: Read part 1.9')
    questions11 = create_textinputquiz_widget('Does pv production cover the consumption outside its period of production?', "answer:",
                                              'no', "!", '[hint]: Read part 1.9')
    questions12 = create_textinputquiz_widget('Is there any import during pv production period?', "answer:",
                                            'yes', "!", '[hint]: Read part 1.9')

    display(questions1)
    display(questions2)
    display(questions3)
    display(questions4)
    display(questions5)
    display(questions6)
    display(questions7)
    display(questions8)
    display(questions9)
    display(questions10)
    display(questions11)
    display(questions12)

quiz()