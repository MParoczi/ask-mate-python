import csv


answer_header = ['id','submission_time','vote_number','question_id','message','image']



def read_file(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


def write_file(file_name, data, header):
    with open(file_name, 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header, restval="None")

        writer.writeheader()

        writer.writerows(data)


def append_data(file_name, dict_to_append):
    data = read_file(file_name)

    data.append(dict_to_append)
    
    write_file(file_name, data, answer_header)
