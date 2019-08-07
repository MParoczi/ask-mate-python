import connection

import calendar
import database_common
import time
from datetime import datetime
from operator import itemgetter
from psycopg2 import sql


from util import question_file_name, question_header,answer_file_name, answer_header



@database_common.connection_handler
def get_data_by_key(cursor, key, data_id, table):
    cursor.execute(
        sql.SQL("select * from {} "
                "where {} = (%s) ").
            format(sql.Identifier(table), sql.Identifier(key)),
            data_id
        )
    row_dict = cursor.fetchall()
    return row_dict


def add_submission_time():
    submission_time = datetime.now()
    return submission_time


#altalanosabban? vote_number re is! mint question/answer table es melyik col
@database_common.connection_handler
def count_views_question(cursor, question_id):
    cursor.execute(
            """ UPDATE question
                SET view_number= view_number + 1
                WHERE id = %(question_id)s;
            """,
        {'question_id': question_id}
        )


def make_new_question(request_function):
    INITIAL_VALUE = 0
    new_question = {'id' : create_new_id(question_file_name),
                    'submission_time': add_submission_time(),
                    'view_number' : INITIAL_VALUE,
                    'vote_number' : INITIAL_VALUE,
                    'title' : request_function.get('question_title'),
                    'message' : request_function.get('question'),
                    'image' : request_function.get('image')}


    connection.append_data(question_file_name, new_question, question_header)


#not working as sqlIdentifier cant take function but only string
@database_common.connection_handler
def insert_new_answer(cursor, request_function, question_id):
    cursor.execute(
        sql.SQL("insert into answer"
                "values ( {submission_time}, 1, "
                "{question_id},{request_function.get('message')}, {request_function.get('image')}").format(
            message = sql.Identifier(request_function.get('message')),
            image = sql.Identifier(request_function.get('image')),
            question_id=sql.Identifier(question_id),
            submission_time=sql.Identifier(add_submission_time()),
        ))




def convert_unix_to_human_time(data_from_csv):
    data = data_from_csv
    rows = []
    for question in data:
        question['submission_time'] = datetime.fromtimestamp(int(question['submission_time']))
        rows.append(question)
    return rows


def edit_question(request_function, question_id):

    data = {'id': question_id,
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

"""
def delete_question_by_id(question_id, key, header, file_name):
    data = connection.read_file(file_name)
    rows = []
    for row in data:
        if question_id == row[key]:
            pass
        else:
            rows.append(row)

    connection.write_file(file_name, rows, header)
"""

@database_common.connection_handler
def delete_question_by_id(cursor, question_id):
    cursor.execute(
        """DELETE FROM question
            WHERE id = %(question_id)s;
        """,
        {'question_id': question_id}
    )


def ordering_dict(title, direction, dict_to_order):
    rev = True
    list_of_dict = []
    for dict in dict_to_order:
        for element in dict:
            if element == 'id' or element == 'view_number' or element == 'vote_number':
                dict[element] = int(dict[element])
        list_of_dict.append(dict)
    if direction == 'ascending':
        rev = False
    if title is None:
        title = 'submission_time'

    new_list = sorted(list_of_dict, key=itemgetter(title), reverse=rev)

    return new_list



@database_common.connection_handler
def get_all_data(cursor, table_name):
    cursor.execute(
            sql.SQL(" select * from {table_name}").format(
                table_name=sql.Identifier(table_name))
            )

    rows = cursor.fetchall()
    return rows



