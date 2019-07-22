import connection


def get_data_by_key(file_name, searching_key, key_to_search):
    data = connection.read_file(file_name)
    result = []
    for row in data:
        if row[key_to_search] == searching_key:
            result.append(row)
    return result
