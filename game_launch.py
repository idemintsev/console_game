# -*- coding: utf-8 -*-
# Use Python3.7

from game_engine import Player, World
from game_loggin import create_dict, write_csv

remaining_time = '123456.0987654321' # Игровое время
field_names = ['current_location', 'current_experience', 'current_date']  # Названия столбцов для лог-файла (csv)

if __name__ == '__main__':
    while True:
        hero = Player('Игорь')
        underground = World(file_with_map='map.json', remaining_time=remaining_time)
        underground.launch_game()
        while not underground.game_over():
            underground.act(hero.experience)
            if underground.attack:
                hero.attack(underground.experience)
                underground.attack = False
            elif underground.go:
                underground.go = False

            game_results = []
            game_results.append(underground.current_location)
            game_results.append(hero.experience)
            game_results.append(underground.current_date_time)
            data_to_csv = create_dict(name_for_head=field_names, element_for_values=game_results)
        write_csv(names_for_head=field_names, data_to_write=data_to_csv)

        print('\nКонец игры\n')

        while True:
            print('Желаете начать сначала?')
            answer = input('\ny/n >>> ')
            if answer not in ['y', 'n']:
                print('Некорректный ввод\n')
            else:
                break
        if answer == 'y':
            continue
        else:
            break

    print('\nВы вышли из игры')