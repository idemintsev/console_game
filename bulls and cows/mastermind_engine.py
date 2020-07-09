from random import randint

number = ''
result = {}


def get_number():
    global number
    number = ''
    number += str(randint(1, 9))
    while len(number) < 4:
        _num = str(randint(0, 9))
        if _num not in number:
            number += _num
    return number


def check_user_answer(user_answer):
    global result
    result = {'быки': None, 'коровы:': None}
    bulls, cows = 0, 0
    for _num, value in enumerate(user_answer):
        if value == number[_num]:
            bulls += 1
        elif number.find(value) != -1:
            cows += 1
    result = {'быки': bulls, 'коровы': cows}
    for key, value in result.items():
        print(f'{key} - {value}')
    return result


def is_game_over():
    return result['быки'] == 4
