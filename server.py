from flask import Flask, render_template, request, redirect, url_for

import data_manager

import connection


from util import question_header, question_file_name, answer_header, answer_file_name, order_directions, order_parameter


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    data = data_manager.get_all_data('question')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    result = data_manager.ordering_dict(order_by, order_direction, data)

    return render_template('list.html',
                           questions=result,
                           question_header=question_header,
                           order_directions=order_directions,
                           order_by=order_by,
                           order_direction=order_direction,
                           order_parameter=order_parameter,
                           )

@app.route('/list-database')
def route_list_database():
    data = data_manager.get_all_data('question')
    return render_template('list_database.html', data=data)

@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):

    if request.method == 'GET':
        data_manager.count_views_question(question_id)
    else:
        data_manager.insert_new_answer(request.form, question_id)

    row=data_manager.get_data_by_key('id', question_id, 'question')
    answers=data_manager.get_data_by_key('question_id', question_id, 'answer')
    return render_template('display_question.html', question=row, answers=answers, question_id=question_id)

@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        data_manager.make_new_question(request.form)

        return redirect('/')

    return render_template('add_question.html')


@app.route('/question/<question_id>/add-new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        data_manager.insert_new_answer(request.form, question_id)
        return redirect('/question/<question_id>')
    return render_template('add_new_answer.html', question_id=question_id)


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.delete_question_by_id(question_id, 'id', question_header, question_file_name)
        data_manager.delete_question_by_id(question_id, 'question_id', answer_header, answer_file_name)

        return redirect('/list')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_question_edit(question_id):
    if request.method == 'GET':
        row = data_manager.get_data_by_key(question_file_name, question_id, 'id')
        return render_template('question_edit.html', rows=row, question_id=question_id)
    else:
        data_manager.edit_question(request.form, question_id)
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
