from flask import Flask, request, flash, render_template, redirect
from surveys import satisfaction_survey


app = Flask(__name__)

responses = []

@app.route('/')
def survey_form():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('survey_form.html', title=title, instructions=instructions)

@app.route('/questions<int:qnumb>', methods=['GET', 'POST'])
def question(qnumb):
    current_choice = satisfaction_survey.questions[qnumb].choices
    current_question = satisfaction_survey.questions[qnumb].question

    if len(responses) != qnumb:
        return redirect(f'/questions{len(responses)}')

    
    return render_template('questions.html', current_choice=current_choice, current_question=current_question)

@app.route('/answer', methods=['POST'])
def get_answer():
    choice = request.form['answer']
    responses.append(choice)
    question_location = len(responses)

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/finished")
    else:
        return redirect(f'/questions{question_location}')


@app.route('/finished')
def finished_survey():
    responses.clear()
    return "Your response has been recorded.Thank you for completing this survey!"