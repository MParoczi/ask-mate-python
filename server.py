from flask import Flask, render_template, request, redirect, url_for

import data_manager

import connection

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = connection.read_file('sample_data/question.csv')
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def route_question(question_id):
    row = data_manager.get_data_by_key('sample_data/question.csv', question_id, 'id')
    answers = data_manager.get_data_by_key('sample_data/answer.csv', question_id, 'question_id')
    return render_template('display_question.html', question=row, answers=answers)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    return render_template('add_question.html')


if __name__ == '__main__':
    app.run(debug=True)
