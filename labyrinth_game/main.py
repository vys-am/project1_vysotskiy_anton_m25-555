#!/usr/bin/env python3
# labyrinth_game/main.py

from .player_actions import get_input, show_inventory, move_player, take_item, use_item
from .utils import (  # noqa: E501
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)
#

# Функция обработки команд
def process_command(game_state: dict, command: str) -> None:
    '''
    game_state - текущее состояние игры,
    command - введенная команда
    '''
    splited_command = command.split()

    match splited_command[0].lower():
        case "look":
            describe_current_room(game_state=game_state)

        case "use":
            if len(splited_command) > 1:
                use_item(game_state=game_state, item_name=splited_command[1].lower())
            else:
                print("Не указан предмет для использования")

        case "go":
            if len(splited_command) > 1:
                move_player(game_state=game_state, direction=splited_command[1].lower())
            else:
                print("Не указано направление движения.")

        case "take":
            if len(splited_command) > 1:
                take_item(game_state=game_state, item_name=splited_command[1].lower())
            else:
                print("Не указан предмет для поднятия.")

        case "inventory":
            show_inventory(game_state=game_state)

        case "solve":
            if game_state['current_room'] == "treasure_room":
                attempt_open_treasure(game_state=game_state)

            else:
                solve_puzzle(game_state=game_state)

        case "quit":
            game_state['game_over'] = True
            print("Выход из игры.")

        case "exit":
            game_state['game_over'] = True
            print("Выход из игры.")

        case "help":
            show_help()

        case _:
            if splited_command[0].lower() in ["north", "south", "east", "west"]:
                move_player(game_state=game_state, direction=splited_command[0].lower())
            else:
                print("Неверная команда!")
                show_help()

# Основная функуия
def main():
    game_state = {
            'player_inventory': [], # Инвентарь игрока
            'current_room': 'entrance', # Текущая комната
            'game_over': False, # Значения окончания игры
            'steps_taken': 0 # Количество шагов
    }

    print("\nДобро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state=game_state)

    while not game_state['game_over']:
        user_cmd = get_input()
        process_command(game_state=game_state, command=user_cmd)

# Основное тело
if __name__ == "__main__":
    main()
  
  