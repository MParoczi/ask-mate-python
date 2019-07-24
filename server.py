from flask import Flask, render_template, request, redirect, url_for

import data_manager

import connection


from util import question_header, question_file_name, answer_header, answer_file_name


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = reversed(connection.read_file(question_file_name))
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):

    if request.method == 'GET':
        data_manager.count_views_question(question_id)

        row = data_manager.get_data_by_key(question_file_name, question_id, 'id')
        answers = data_manager.get_data_by_key(answer_file_name, question_id, 'question_id')
        return render_template('display_question.html', question=row, answers=answers, question_id=question_id)
    else:
        id = data_manager.create_new_id(answer_file_name)
        submission_time = data_manager.add_submission_time()
        data = {'message': request.form.get('message'),
                'question_id': question_id,
                'id': id,
                'submission_time': submission_time}
        connection.append_data(answer_file_name, data, answer_header)

        row = data_manager.get_data_by_key(question_file_name, question_id, 'id')
        answers = data_manager.get_data_by_key(answer_file_name, question_id, 'question_id')
        return render_template('display_question.html', question=row, answers=answers)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        INITIAL_VIEW = 0
        new_question = {}

        new_question['id'] = data_manager.create_new_id(question_file_name)
        new_question['submission_time'] = data_manager.add_submission_time()
        new_question['view_number'] = INITIAL_VIEW
        new_question['title'] = request.form['question_title']
        new_question['message'] = request.form['question']

        connection.append_data(question_file_name, new_question, question_header)

        return redirect('/')

    return render_template('add_question.html')


@app.route('/question/<question_id>/add-new-answer')
def route_new_answer(question_id):
    return render_template('add_new_answer.html', question_id=question_id)


if __name__ == '__main__':
    app.run(debug=True)
