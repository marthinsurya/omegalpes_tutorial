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
            s = "Congratulation! You have finished tutorial 1. Check your answer : 1, 24, 4, 2, 2, 1, 1, yes, yes, 4, no, yes"

        else:
            s = "You are not trying to guess, aren't you? Check the hint!"
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
    questions = create_textinputquiz_widget('What is the magic sentence?', "answer:", 'JOHN HATES BROCOLLI', "!",
                                            '[hint]: Form a sentence from the magic words you collected from this tutorial 1')

    display(questions)

quiz()