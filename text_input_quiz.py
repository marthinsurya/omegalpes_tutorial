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
            s = '\x1b[6;30;42m' + "correct" + '\x1b[0m' + "\n"  # green color

        else:
            s = '\x1b[5;30;41m' + "try again" + '\x1b[0m' + "\n"  # red color
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
    #question_prompts = [
    #    "How much energy was imported from the grid?\n",
    #    "How much energy was consumed from the PV?\n",
    #    "How many energy units are there in the energy system?\n"]
    #answers = ['1','2','3']
    #questions = create_textinputquiz_widget(question_prompts, "answer:", answers, "kWh",
    #                                        '[hint]:Omegalpes code line')
    questions = create_textinputquiz_widget('How much energy was imported?',"answer:",'123',"kWh",'[hint]:Omegalpes code line')

    display(questions)

quiz()