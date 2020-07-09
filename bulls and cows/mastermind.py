# -*- coding: utf-8 -*-

from mastermind_engine import get_number, check_user_answer, is_game_over

number_of_trying = 0
get_number()

while True:
    while True:
        user_answer = input('Введите четырехзначное число >>> ')
        if user_answer.isdigit() and len(user_answer) == 4:
            if user_answer[0] != '0':
                if len(set(user_answer)) == 4:
                    break
        print('Некорректный ввод!')

    check_user_answer(user_answer)
    number_of_trying += 1
    if is_game_over():
        print(f'Поздравляем, вы угадали! Количество попыток - {number_of_trying}')
        while True:
            game_continue = input('Хотите еще партию? y/n >>> ')
            if game_continue.casefold() == 'y':
                get_number()
                break
            elif game_continue.casefold() == 'n':
                exit()
            else:
                print('Некорректный ввод!')
