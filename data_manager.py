import connection

import calendar

import time

from util import question_file_name, question_header


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
    INITIAL_VIEW = 0
    new_question = {}

    new_question['id'] = create_new_id(question_file_name)
    new_question['submission_time'] = add_submission_time()
    new_question['view_number'] = INITIAL_VIEW
    new_question['title'] = request_function['question_title']
    new_question['message'] = request_function['question']

    connection.append_data(question_file_name, new_question, question_header)
