from flask import Flask, render_template, request, redirect, url_for, session, flash

import data_manager

from util import question_header, order_directions, order_parameter


app = Flask(__name__)

app.secret_key = b' \xd4\x14\xf1\xbe\x0e\x91@\x11\x9f\xe5\xacp\xd8\xf0\xf5'


@app.route('/')
@app.route('/latest_five_question')
def route_list_of_first_five_question():
    questions = data_manager.get_latest_five_question()
    if 'user_id' in session:

        return render_template('list_of_first_five.html', questions=questions, guest=False)

    return render_template('list_of_first_five.html', questions=questions, guest=True)


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


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):

    if request.method == 'GET':
        data_manager.count_views_question(question_id)
    else:
        if 'user_id' in session:
            if request.method == 'POST':
                data_manager.insert_new_answer(request.form, question_id, session['user_id'])
                return redirect(f'/question/{question_id}')
            return render_template('add_new_answer.html', question_id=question_id)
        return redirect('/login')

    question_comments = data_manager.get_comments_by_question_id(question_id)
    row = data_manager.get_data_by_key('id', question_id, 'question')
    answers = data_manager.get_data_by_key('question_id', question_id, 'answer')
    comments = data_manager.get_comments_of_answers()

    verified = False
    if 'user_id' in session:
        user_id_from_db = data_manager.get_user_id(question_id)
        if user_id_from_db['user_id'] == session['user_id']:
            verified = True

        return render_template('display_question.html', question=row, answers=answers, question_id=question_id, comments=comments, question_comments=question_comments, verified=verified, user_id=session['user_id'])
    return render_template('display_question.html', question=row, answers=answers, question_id=question_id,
                           comments=comments, question_comments=question_comments)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if 'user_id' in session:
        if request.method == 'POST':
            data_manager.make_new_question(request.form, session['user_id'])
            return redirect('/')
        return render_template('add_question.html')

    return redirect('/login')


@app.route('/question/<question_id>/add-new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if 'user_id' in session:
        if request.method == 'POST':
            data_manager.insert_new_answer(request.form, question_id, session['user_id'])
            return redirect(f'/question/{question_id}')
        return render_template('add_new_answer.html', question_id=question_id)
    return redirect('/login')


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.delete_question_by_id(question_id)

        return redirect('/list')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_question_edit(question_id):
    if request.method == 'GET':
        row = data_manager.get_data_by_key('id', question_id, 'question')
        return render_template('question_edit.html', rows=row, question_id=question_id)

    data_manager.edit_question(request.form, question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(answer_id):
    if request.method == 'GET':
        row = data_manager.get_data_by_key('id', answer_id, 'answer')
        return render_template('answer_edit.html', rows=row, answer_id=answer_id)
    else:
        data_manager.edit_answer(request.form, answer_id)
        return redirect('/')


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def route_add_comment_to_question(question_id):
    if 'user_id' in session:
        if request.method == 'POST':
            data_manager.add_comment_to_question(request.form, question_id, session['user_id'])

            return redirect(url_for('route_question', question_id=question_id))


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def route_new_comment_for_answer(answer_id):
    if 'user_id' in session:
        if request.method == 'POST':
            question_id = data_manager.get_question_id_from_answer(answer_id)
            data_manager.add_new_comment_to_answer(request.form, answer_id, session['user_id'])
            return redirect(url_for('route_question', question_id=question_id))


@app.route('/comments/<comment_id>/delete')
def route_delete_comment(comment_id):
    question_id = data_manager.get_question_id_from_comment(comment_id)
    data_manager.delete_comment(comment_id)
    return redirect(url_for('route_question', question_id=question_id))


@app.route('/question/<question_id>/vote', methods=['GET', 'POST'])
def route_vote(question_id):
    if request.method == "POST":
        if request.form.get('vote') == "up":
            data_manager.count_vote_up(question_id)
        else:
            data_manager.count_vote_down(question_id)
        return redirect(url_for('route_question', question_id=question_id))


@app.route('/sign_up', methods=['GET', 'POST'])
def route_sign_up():
    if request.method == 'POST':
        for name in data_manager.get_all_user_name():
            if name['user_name'] == request.form.get('user_name'):
                return render_template('sign_up.html', occupied=True, guest=True)
        data_manager.save_new_user(request.form)
        return redirect('/')
    else:
        return render_template('sign_up.html', sign_up=True, guest=True)


@app.route('/login', methods=['POST', 'GET'])
def route_login():
    if request.method == 'POST':
        try:
            is_matching = data_manager.verify_user(request.form)
        except TypeError:
            is_matching = False
        if is_matching:
            user_id = data_manager.get_user_id_by_name(request.form)
            session['user_id'] = user_id
            session['user_name'] = request.form.get('user_name')
            return redirect('/')
        else:
            return render_template('sign_up.html', wrong=True, guest=True)
    else:
        return render_template('sign_up.html', sign_up=False, guest=True)


@app.route('/logout')
def route_logout():
    session.pop('user_id', None)
    session.pop('user_name')
    return redirect('/')


@app.route('/list-users')
def route_list_users():
    users_dict = data_manager.get_all_users()
    return render_template('list_users.html', users_dict=users_dict)

if __name__ == '__main__':
    app.run(debug=True)
