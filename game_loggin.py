
# Use Python3.7

import csv


# Функции get_data_to_csv и create_dict служат для создания списка словарей,
# которые будут записаны в csv-файл по итогам игры.


def get_data_to_csv(function):
    _data_to_csv = []

    def func(*args, **kwargs):
        _data_to_csv.append(function(*args, **kwargs))
        return _data_to_csv

    return func


@get_data_to_csv
def create_dict(name_for_head: list, element_for_values: list):
    _dictionary = dict(zip(name_for_head, element_for_values))
    return _dictionary


def write_csv(names_for_head: list, data_to_write: list, csv_file_name='game_log.csv'):
    """
    Записывает данные игры в csv-файл.
    :param names_for_head: переменная с названиями столбцов для csv-файла.
    :param data_to_write: переменная с данными для записи в csv-файл  [{'':'', '':'', '':''}, {'':'', '':'', '':''} ...]
    :param csv_file_name: имя csv-файла.
    """

    with open(csv_file_name, 'a', newline='') as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(names_for_head)

    with open(csv_file_name, 'a', newline='') as out_csv:
        writer = csv.DictWriter(out_csv, delimiter=',', fieldnames=names_for_head)
        for element in data_to_write:
            writer.writerow(element)
