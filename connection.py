import csv


def read_file(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


def write_file(file_name):
    pass