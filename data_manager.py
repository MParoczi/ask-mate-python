import database_common

from datetime import datetime

from operator import itemgetter

from psycopg2 import sql



@database_common.connection_handler
def get_data_by_key(cursor, key, data_id, table):
    cursor.execute(
        sql.SQL("select * from {table} "
                "where {key} = (%s) ").
            format(table=sql.Identifier(table), key=sql.Identifier(key)),
        [data_id]
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
            VALUES (%s, %s ,%s, %s,%s, %s)
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

@database_common.connection_handler
def edit_answer(cursor, request_function, answer_id):
    vote_number = request_function.get('vote_number')
    question_id = request_function.get('answer_id')
    message = request_function.get('message')
    image = request_function.get('image')

    cursor.execute(
        """UPDATE answer 
           SET id = %(answer_id)s,
               vote_number = %(vote_number)s,
              message = %(message)s,
              image = %(image)s
           WHERE id = %(answer_id)s;
        """,
        {'answer_id': answer_id,
         'vote_number': vote_number,
         'question_id': question_id,
         'message': message,
         'image': image,
         }
    )


@database_common.connection_handler
def add_comment_to_question(cursor, request_function, question_id):
    submission_time = add_submission_time()
    message = request_function.get('new_comment')

    cursor.execute(
        """INSERT INTO comment (question_id, message, submission_time) 
            VALUES (%(question_id)s, %(message)s, %(submission_time)s)
        """,
        {
            'question_id': question_id,
            'submission_time': submission_time,
            'message': message,
        }
    )
@database_common.connection_handler
def get_comments_by_question_id(cursor, question_id):
    cursor.execute(
        """SELECT id, question_id, answer_id, message, submission_time, edited_count FROM comment
            WHERE question_id = %(question_id)s
        """,
        {'question_id': question_id}
    )
    comments = cursor.fetchall()
    return comments

@database_common.connection_handler
def get_comments_of_answers(cursor):
    cursor.execute(
        sql.SQL("""
                SELECT * FROM comment
                """))
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def add_new_comment_to_answer(cursor, request_function, answer_id):
    cursor.execute(
        sql.SQL("""
                INSERT INTO comment (answer_id, message, submission_time)
                 VALUES (%s, %s, %s)
                 """),
                    [answer_id,
                    request_function.get('new_comment'),
                    add_submission_time()])


@database_common.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute(
        sql.SQL("""
        DELETE FROM comment WHERE id = %s"""),
        [comment_id]
    )


@database_common.connection_handler
def get_question_id_from_comment(cursor, comment_id):
    cursor.execute(
        sql.SQL("""SELECT question_id
                    FROM comment
                    WHERE id = %s"""),
        [comment_id]
    )

    id = cursor.fetchone()
    if id['question_id'] is not None:
        return id['question_id']
    else:
        cursor.execute(
            sql.SQL("""SELECT DISTINCT answer.question_id
                        FROM answer
                        INNER JOIN comment
                        ON answer.id = comment.answer_id
                        WHERE comment.id = %s"""),
            [comment_id]
        )
        id = cursor.fetchone()
        return id['question_id']


@database_common.connection_handler
def get_question_id_from_answer(cursor, answer_id):
    cursor.execute(
        sql.SQL("""
                SELECT question_id
                FROM answer
                WHERE id = %s"""),
                [answer_id]
    )
    id = cursor.fetchone()
    return id['question_id']

@database_common.connection_handler
def count_vote_up(cursor, question_id):
    cursor.execute(
        """ UPDATE question
            SET vote_number= vote_number + 1
            WHERE id = %(question_id)s;
        """,
        {'question_id': question_id}
    )


@database_common.connection_handler
def count_vote_down(cursor, question_id):
    cursor.execute(
        """ UPDATE question
            SET vote_number= vote_number - 1
            WHERE id = %(question_id)s;
        """,
        {'question_id': question_id}
    )
