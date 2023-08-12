from flask import Flask, request, flash, render_template, redirect, session
from surveys import satisfaction_survey
RESPONSES_KEY = 'responses'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret99'



@app.route('/')
def survey_form():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('survey_form.html', title=title, instructions=instructions)

@app.route('/start', methods=["POST"])
def set_seession():
    session[RESPONSES_KEY] = []
    return redirect('/questions0')

@app.route('/questions<int:qnumb>', methods=['GET', 'POST'])
def question(qnumb):
    if qnumb > len(satisfaction_survey.questions):
        return redirect('/')
    
    current_choice = satisfaction_survey.questions[qnumb].choices
    current_question = satisfaction_survey.questions[qnumb].question
    responses = session.get(RESPONSES_KEY)
 
    if len(responses) != qnumb:
        return redirect(f'/questions{len(responses)}')
    
    return render_template('questions.html', current_choice=current_choice, current_question=current_question)

@app.route('/answer', methods=['POST'])
def get_answer():
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    question_location = len(responses)

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/finished")
    else:
        return redirect(f'/questions{question_location}')


@app.route('/finished')
def finished_survey():
    return "Your response has been recorded.Thank you for completing this survey!"