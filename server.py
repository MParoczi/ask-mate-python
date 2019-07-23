from flask import Flask, render_template, request, redirect, url_for

import data_manager

import connection

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = reversed(connection.read_file('sample_data/question.csv'))
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):
    data_manager.count_views_question(question_id)

    if request.method == 'GET':

        row = data_manager.get_data_by_key('sample_data/question.csv', question_id, 'id')
        answers = data_manager.get_data_by_key('sample_data/answer.csv', question_id, 'question_id')
        return render_template('display_question.html', question=row, answers=answers, question_id=question_id)
    else:
        id = data_manager.create_new_id('sample_data/answer.csv')
        submission_time = data_manager.add_submission_time()
        data = {'message': request.form.get('message'),
                'question_id': question_id,
                'id': id,
                'submission_time': submission_time}
        connection.append_data('sample_data/answer.csv', data, connection.answer_header)

        row = data_manager.get_data_by_key('sample_data/question.csv', question_id, 'id')
        answers = data_manager.get_data_by_key('sample_data/answer.csv', question_id, 'question_id')
        return render_template('display_question.html', question=row, answers=answers)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        INITIAL_VIEW = 0
        new_question = {}

        new_question['id'] = data_manager.create_new_id('sample_data/question.csv')
        new_question['submission_time'] = data_manager.add_submission_time()
        new_question['view_number'] = INITIAL_VIEW
        new_question['title'] = request.form['question_title']
        new_question['message'] = request.form['question']

        connection.append_data('sample_data/question.csv', new_question, data_manager.question_headers)

        return redirect('/')

    return render_template('add_question.html')


@app.route('/question/<question_id>/add-new-answer')
def route_new_answer(question_id):
    return render_template('add_new_answer.html', question_id=question_id)


if __name__ == '__main__':
    app.run(debug=True)
