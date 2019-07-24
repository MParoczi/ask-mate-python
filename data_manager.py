import connection

import calendar

import time
from datetime import datetime

from util import question_file_name, question_header,answer_file_name, answer_header


def get_data_by_key(file_name, searching_key, key_to_search):
    data = connection.read_file(file_name)
    result = []
    for row in data:
        if row[key_to_search] == searching_key:
            result.append(row)
    return result


def create_new_id(file_name):
    NEW_ID = 1
    data = connection.read_file(file_name)
    highest_id = int(max(data, key=lambda x: int(x['id']))['id'])
    return highest_id + NEW_ID


def add_submission_time():
    submission_time = calendar.timegm(time.gmtime())
    return submission_time


def count_views_question(question_id):
    data_to_modify = connection.read_file(question_file_name)
    rows = []
    NEW_VIEW = 1

    for row in data_to_modify:
        if question_id == row['id']:
            row['view_number'] = int(row['view_number']) + NEW_VIEW
        rows.append(row)

    connection.write_file(question_file_name, rows, question_header)


def make_new_question(request_function):
    INITIAL_VALUE = 0
    new_question = {}

    new_question['id'] = create_new_id(question_file_name)
    new_question['submission_time'] = add_submission_time()
    new_question['view_number'] = INITIAL_VALUE
    new_question['vote_number'] = INITIAL_VALUE
    new_question['title'] = request_function['question_title']
    new_question['message'] = request_function['question']


    connection.append_data(question_file_name, new_question, question_header)


def make_new_answer(request_function, question_id):
    INITIAL_VALUE = 0
    id = create_new_id(answer_file_name)
    submission_time = add_submission_time()
    data = {'id': id,
            'submission_time': submission_time,
            'vote_number': INITIAL_VALUE,
            'question_id': question_id,
            'message': request_function.get('message'),
            'image': request_function.get('image')}
    connection.append_data(answer_file_name, data, answer_header)


def convert_unix_to_human_time(data_from_csv):
    data = data_from_csv
    rows = []
    for question in data:
        question['submission_time'] = datetime.fromtimestamp(int(question['submission_time']))
        rows.append(question)
    return rows


def edit_question(request_function, question_id):

    data = {'id': question_id,
            'submission_time': request_function.get('submission_time'),
            'view_number': request_function.get('view_number'),
            'vote_number': request_function.get('vote_number'),
            'title': request_function.get('title'),
            'message': request_function.get('message'),
            'image': request_function.get('image')}

    data_to_modify = connection.read_file(question_file_name)

    for row in data_to_modify:
        if row['id'] == data['id']:
            row.update(data)

    connection.write_file(question_file_name, data_to_modify, question_header)


def delete_question_by_id(question_id):
    q_data = connection.read_file(question_file_name)
    rows = []
    for row in q_data:
        if question_id == row['id']:
            pass
        else:
            rows.append(row)

    connection.write_file(question_file_name, rows, question_header)

    a_data = connection.read_file(answer_file_name)
    rows = []
    for row in a_data:
        if question_id == row['question_id']:
            pass
        else:
            rows.append(row)

    connection.write_file(answer_file_name, rows, answer_header)


