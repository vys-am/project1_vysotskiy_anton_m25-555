# labyrinth_game/constants.py

# Константа с описанием комнат
ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта. Стены покрыты мхом. На полу лежит старый факел.', # noqa: E501
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None 
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.', # noqa: E501
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room', 'east': 'corridor'}, # noqa: E501
        'items': [],
        'puzzle': ('На пьедестале надпись: "Назовите число, которое идет после девяти". Введите ответ цифрой или словом.', '10') # noqa: E501
    },
    'trap_room': {
          'description': 'Комната с хитрой плиточной поломкой. На стене видна надпись: "Осторожно — ловушка".', # noqa: E501
          'exits': {'west': 'entrance', 'north': 'corridor'},
          'items': ['rusty_key'],
          'puzzle': ('Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд (введите "шаг шаг шаг")', 'шаг шаг шаг') # noqa: E501
    },
    'library': {
          'description': 'Пыльная библиотека. На полках старые свитки. Где-то здесь может быть ключ от сокровищницы.', # noqa: E501
          'exits': {'east': 'hall', 'north': 'armory'},
          'items': ['ancient_book'],
          'puzzle': ('В одном свитке загадка: "Что растет, когда его съедают?" (ответ одно слово)', 'резонанс') # noqa: E501
    },
        'armory': {
          'description': 'Старая оружейная комната. На стене висит меч, рядом — небольшая бронзовая шкатулка.', # noqa: E501
          'exits': {'south': 'library'},
          'items': ['sword', 'bronze_box'],
          'puzzle': None
    },
    'treasure_room': {
          'description': 'Комната, на столе большой сундук. Дверь заперта — нужен особый ключ.', # noqa: E501
          'exits': {'south': 'hall'},
          'items': ['treasure_chest'],
          'puzzle': ('Дверь защищена кодом. Введите код (подсказка: это число пятикратного шага, 2*5= ? )', '10') # noqa: E501
    },
    # Мои комнаты:
    'corridor': {
        'description': 'Вы в длинном коридоре. Стены украшены гобеленами и картинами с изображениями предков лорда.', # noqa: E501
        'exits': {'west': 'hall', 'south': 'trap_room', 'east': 'bedroom'},
        'items': ['old_armor'],
        'puzzle': None
    },
    'bedroom': {
        'description': 'Вы в покоях лорда. В комнате стоит письменный стол, кровь и огромный камин излучающий приятное тепло.', # noqa: E501
        'exits': {'west': 'corridor'},
        'items': ['old_note'],
        'puzzle': None
    }
}

# Константа с описанием перевода чисел с их словарные версии (для загадок)
NUMBERS = {
    '0': 'ноль',
    '1': 'один',
    '2': 'два',
    '3': 'три',
    '4': 'четыре',
    '5': 'пять',
    '6': 'шесть',
    '7': 'семь',
    '8': 'восемь',
    '9': 'девять',
    '10': 'десять',
}

# Константа с описанием команд
COMMANDS = {
    'go <direction>': 'перейти в направлении (north/south/east/west)',
    '<direction>': 'перейти в направлении (north/south/east/west)',
    'look': 'осмотреть текущую комнату',
    'take <item>': 'поднять предмет',
    'use <item>': 'использовать предмет из инвентаря',
    'inventory': 'показать инвентарь',
    'solve': 'попытаться решить загадку в комнате',
    'quit/exit': 'выйти из игры',
    'help': 'показать это сообщение'
}

# Константы с параметрами для случайных событий
EVENT_PROBABILITY = 10
EVENT_COUNT = 2
EVENT_INTENSIVITY = 4
TRAP_DMG_PROBABILITY = 9
BEAST_DMG_PROBABILITY = 8
EVENT1_DEATH_DMG = 3
EVENT2_DEATH_DMG = 2