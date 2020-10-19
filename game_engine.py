
# Use Python3.7

import datetime, json, os
from decimal import Decimal, getcontext

getcontext().prec = 16  # Установлена точность вычислений для работы с данными класса World


class Player:
    """
    Герой.
    Сражается с монстрами и увеличивает свой опыт после каждого сражениня.
    """

    def __init__(self, name: str):
        self.name = name
        self.experience = 0

    def attack(self, experience):
        self.experience += experience


class World:
    """
    Игровой мир с монстрами и картой подземелья.

    Принимает параметры:
    world_map - имя json-файла с картой мира.
    remaining_time - количество времени, которое есть у игрока.
    path_to_file_with_map - путь до файла с картой. Необязательный параметр.
    """

    def __init__(self, file_with_map: str, remaining_time: str, path_to_file_with_map=None):
        self.map_file_name = file_with_map
        self.path_to_map_file = os.path.dirname(__file__) if path_to_file_with_map is None \
            else os.path.normpath(path_to_file_with_map)
        self.world = os.path.join(self.path_to_map_file, self.map_file_name)
        self.time_limit = remaining_time
        self.level_events = []
        self.current_location, self.current_date_time, self.next_location, self.player_choice = None, None, None, None
        self.key_from_next_location, self.experience, self.time_decimal = None, None, None
        self.star_game_time, self.playing_time = None, None
        self.attack, self.go, self.win, self.exit, self.level_events_update = False, False, False, False, True

    def count_time(self):
        """
        Определяет текущее время и сколько времени прошло с начала игры
        """
        self.current_date_time = datetime.datetime.today()
        self.playing_time = self.current_date_time - self.star_game_time
        self.playing_time = str(self.playing_time)[:-7]
        self.current_date_time = str(self.current_date_time)[:-7]

    def create_world(self):
        """
        Загружает данные из json-файла в self.next_location.
        """
        with open(self.world, 'r') as map:
            data_from_map = map.read()
            self.next_location = json.loads(data_from_map)

    def get_initial_location(self):
        """
        Определяет название начальной локации.
        """
        for location in self.next_location:
            self.current_location = location
            self.key_from_next_location = location

    def get_time_experience(self):
        """
        Определяет сколько времени займет сражение с монстром или переход в другую локацию, а также какое количество
        опыта получит герой.
        Время переводится из str в Decimal.
        В зависимости от выбора активирует режим сражения (self.attack) или ходьбы (self.go).
        """
        if ('Mob_' in self.level_events[self.player_choice]) or ('Boss' in self.level_events[self.player_choice]):
            self.attack, self.level_events_update = True, False
            _, self.experience, _time = self.level_events[self.player_choice].split('_')
            self.experience = int(self.experience[3:])
            self.time_decimal = Decimal(_time[2:])
            self.time_limit = Decimal(self.time_limit)
            self.time_limit -= self.time_decimal
            self.time_limit = str(self.time_limit)
        else:
            self.go, self.level_events_update = True, True
            if 'Hatch_' not in str(*self.level_events[self.player_choice]):
                _0, _1, _time = str(*self.level_events[self.player_choice]).split('_')
                self.time_decimal = Decimal(_time[2:])
                self.time_limit = Decimal(self.time_limit)
                self.time_limit -= self.time_decimal
                self.time_limit = str(self.time_limit)
            else:
                _, _time = str(*self.level_events[self.player_choice]).split('_')
                self.time_decimal = Decimal(_time[2:])
                self.time_limit = Decimal(self.time_limit)
                self.time_limit -= self.time_decimal
                self.time_limit = str(self.time_limit)

    def make_choice(self):
        """
        Выводит на консоль действия, который доступны для игрока в текущей локации (список из json файла) и
        позволяет сделать выбор.
        """
        print('\nВнутри вы видите:')
        for index, element in enumerate(self.level_events):
            if isinstance(element, dict):
                print(index, '- Перейти в другую локацию', str(*element.keys()))
            elif isinstance(element, str):
                print(index, '- Атаковать монстра', element)
            else:
                print(index, '- Сдаться и выйти из игры')

        while True:
            self.player_choice = input('Вы решаете >>> ')
            if self.player_choice.isdigit():
                self.player_choice = int(self.player_choice)
                if not -1 < self.player_choice < len(self.level_events):
                    print('Нет такого действия')
                else:
                    break
            else:
                print('Нет такого действия')

    def act(self, hero_experience):
        """
        Добавляет в список self.level_events все доступные для игрока действия.
        Запускает метод self.make_choice.
        Активирует события текущей локации в зависимости от выбора игрока.
        """
        print('\n', '*' * 10)
        print('Вы находитесь в -', self.current_location)
        print(f'У вас {hero_experience} опыта и осталось {self.time_limit} секунд до наводнения')
        self.count_time()
        print(f'Прошло уже {self.playing_time}')
        if self.level_events_update:
            for element in self.next_location[self.key_from_next_location]:
                self.level_events.append(element)
            self.level_events.append(None)  # Будет использоваться для возможности прервать игру
        self.make_choice()

        if self.level_events[self.player_choice] is not None:
            if isinstance(self.level_events[self.player_choice], dict):
                if 'Hatch_' in str(*self.level_events[self.player_choice].keys())[:6]:
                    if hero_experience >= 280:
                        print(*self.level_events[self.player_choice].values())
                        self.time_limit = 0
                        self.win = True
                    else:
                        print('\nУ героя недостаточно опыта!\n')
                else:
                    self.get_time_experience()
                    if self.attack:
                        self.level_events.pop(self.player_choice)

                    elif self.go:
                        self.next_location = self.level_events[self.player_choice]
                        self.key_from_next_location = str(*self.next_location.keys())
                        self.level_events.clear()
                        self.current_location = self.key_from_next_location
            else:
                self.get_time_experience()
                if self.attack:
                    self.level_events.pop(self.player_choice)

                elif self.go:
                    self.next_location = self.level_events[self.player_choice]
                    self.key_from_next_location = str(*self.next_location.keys())
                    self.level_events.clear()
                    self.current_location = self.key_from_next_location
        else:
            self.time_limit = 0
            self.exit = True

    def game_over(self):
        zero = Decimal(0)
        time_limit = Decimal(self.time_limit)
        if time_limit <= zero:
            if self.win:
                return True
            else:
                if self.exit:
                    return True
                else:
                    print('Наводнение! Пещеру затопило!')
                    return True
        else:
            return False

    def launch_game(self):
        self.star_game_time = datetime.datetime.today()
        self.create_world()
        self.get_initial_location()
