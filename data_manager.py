import connection
import database_common
from datetime import datetime
from operator import itemgetter
from psycopg2 import sql

from util import question_file_name, question_header, answer_header


@database_common.connection_handler
def get_data_by_key(cursor, key, data_id, table):
    cursor.execute(
        sql.SQL("select * from {table} "
                "where {key} = (%s) ").
            format(table=sql.Identifier(table), key=sql.Identifier(key)),
        data_id
    )
    row_dict = cursor.fetchall()
    return row_dict


def add_submission_time():
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return submission_time


@database_common.connection_handler
def count_views_question(cursor, question_id):
    cursor.execute(
        """ UPDATE question
            SET view_number= view_number + 1
            WHERE id = %(question_id)s;
        """,
        {'question_id': question_id}
    )


@database_common.connection_handler
def make_new_question(cursor, request_function):
    cursor.execute(
        sql.SQL(
            """
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        ), [add_submission_time(),
            0,
            0,
            request_function.get('question_title'),
            request_function.get('question'),
            request_function.get('image')]

    )


@database_common.connection_handler
def insert_new_answer(cursor, request_function, question_id):
    cursor.execute(
        sql.SQL(
            "insert into answer (submission_time, vote_number, question_id, message, image) values ( %s, %s, %s, %s, %s ) ").format(),
        [add_submission_time(), 0, question_id, request_function.get('message'), request_function.get('image')]
    )


@database_common.connection_handler
def edit_question(cursor, request_function, question_id):
    view_number = request_function.get('view_number')
    vote_number = request_function.get('vote_number')
    title = request_function.get('title')
    message = request_function.get('message')
    image = request_function.get('image')


    cursor.execute(
        """UPDATE question 
           SET view_number = %(view_number)s,
            vote_number = %(vote_number)s,
             title = %(title)s,
              message = %(message)s,
              image = %(image)s
              
           WHERE id = %(question_id)s;
        """,
        {'question_id': question_id,
         'view_number': view_number,
         'vote_number': vote_number,
         'title': title,
         'message': message,
         'image': image,
         }
    )


@database_common.connection_handler
def delete_question_by_id(cursor, question_id):
    cursor.execute(
        """DELETE FROM answer
            WHERE question_id = %(question_id)s;
            DELETE FROM question
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


@database_common.connection_handler
def get_latest_five_question(cursor):
    cursor.execute("""
                      SELECT id, submission_time, view_number, vote_number, title, message, image FROM question
                      ORDER BY submission_time DESC LIMIT 5;
                """, )

    data = cursor.fetchall()
    return data
