# labyrinth_game/utils.py

import math as ma

# Обозначаем куда смотреть 
from .constants import (
    ROOMS,
    NUMBERS
)

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 
    

# Функция описания текущей комнаты
def describe_current_room(game_state: dict) -> None:
    '''
    game_state - текущее состояние игры
    '''
    current_player_room = game_state['current_room']
    current_room_info = ROOMS[current_player_room]

    print(f"\n== {current_player_room.upper()} ==")

    if len(current_room_info['items']) > 0:
        print(f"Заметные предметы: {', '.join(current_room_info['items'])}") # noqa: E501
    else:
        print("В комнате не видно никаких предметов.")


    print(f"Выходы: {', '.join([i + ' - ' + current_room_info['exits'][i] for i in current_room_info['exits']])}") # noqa: E501

    if current_room_info['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")
    else:
        print("Загадок здесь нет.")

    
def solve_puzzle(game_state):
    # Получаем название текущей комнаты из состояния игры
    current_room_name = game_state['current_room']
    
    # Получаем детали текущей комнаты (загадки)
    current_room_details = ROOMS[current_room_name]['puzzle']

    if not current_room_details:
        print('Загадок здесь нет.')
    else:
        print(current_room_details[0])
        users_answer = input("Ваш ответ: ")
    
        if (users_answer.lower() == current_room_details[1].lower() or current_room_details[1] in NUMBERS and NUMBERS[current_room_details[1]] == users_answer.lower()): # noqa: E501
            print("Загадка решена правильно!")
            current_room_details = None
          
            if current_room_name == "hall":
                game_state['player_inventory'].append('coin')
            
            elif game_state['current_room'] == "trap_room":
                game_state['player_inventory'].append('stick')
          
            elif game_state['current_room'] == "library":
                game_state['player_inventory'].append('big_book')
          
            print(f"Ваша награда: {game_state['player_inventory'][-1]}")
          
        else:
            
            if current_room_name == "trap_room":
                a=123
            # trigger_trap(game_state=game_state)
            
            else:
                print("Неверно. Попробуйте снова.")



# Функция попытки открытия сундука с сокровищами
def attempt_open_treasure(game_state: dict) -> None:
    '''
    game_state - текущее состояние игры
    '''
    # Получаем название текущей комнаты из состояния игры
    current_room_name = game_state['current_room']
    
    # Получаем детали текущей комнаты (предмет)
    current_room_details = ROOMS[current_room_name]['items']

    if "treasure_key" in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        current_room_details.remove('treasure_chest')
        print(f"В сундуке сокровище! Вы победили за {game_state['steps_taken']} шагов!")
        game_state['game_over'] = True

    else:
        users_answer = input("Сундук заперт. ... Ввести код? (да/нет) ")

        if users_answer.lower() == "да":
            users_code = input("Введние код: ")

            if users_code == ROOMS[game_state['current_room']]['puzzle'][1]:
                print("Вы правильно вводите код, и замок щёлкает. Сундук открыт!")
                print(f"В сундуке сокровище! Вы победили за {game_state['steps_taken']} шагов!")
                game_state['game_over'] = True

            else:
                print("Вы ввели неверный код, попробуйте еще раз.")

        else:
            print("Вы отступаете от сундука.")


# Функция склонения предметов
def get_subject_form_in_inventory(count):
    """
    Склоняет слово "предмет" в зависимости от числа.

    Args:
        count (int): Число.

    Returns:
        str: Склоненное слово "предмет".
    """
    if not isinstance(count, int):
        return "Ошибка: на входе не целое число"

    # Получаем последние две цифры числа
    last_two_digits = count % 100
    # Получаем последнюю цифру числа
    last_digit = count % 10

    # Специальный случай для чисел от 11 до 19
    if 11 <= last_two_digits <= 19:
        return "предметов"
    # Для остальных случаев
    elif last_digit == 1:
        return "предмет"
    elif last_digit in [2, 3, 4]:
        return "предмета"
    else:
        return "предметов"
