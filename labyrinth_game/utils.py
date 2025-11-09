# labyrinth_game/utils.py

# Импорт библиотеки
import math as ma

# Обозначаем куда смотреть внутри наших файлов
from .constants import (
    BEAST_DMG_PROBABILITY,
    EVENT1_DEATH_DMG,
    EVENT2_DEATH_DMG,
    EVENT_COUNT,
    EVENT_INTENSIVITY,
    EVENT_PROBABILITY,
    NUMBERS,
    ROOMS,
    TRAP_DMG_PROBABILITY,
)


# Готовые команды для хелпа
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

    print(f"\n== {game_state['current_room'].upper()} ==")

    if len(ROOMS[game_state["current_room"]]["items"]) > 0:
        print(f"Предметы в комнате: {', '.join(ROOMS[game_state['current_room']]['items'])}") # noqa: E501
    else:
        print("В комнате нет полезных предметов.")

    print(f"Выходы: {', '.join([i + ' - ' + ROOMS[game_state['current_room']]['exits'][i] for i in ROOMS[game_state['current_room']]['exits']])}") # noqa: E501

    if not ROOMS[game_state["current_room"]]["puzzle"]:
        print("Загадок здесь нет.")
    else:
        print("Кажется, здесь есть загадка (используйте команду solve).")

    
def solve_puzzle(game_state: dict) -> None:
    '''
    game_state - текущее состояние игры
    '''
    if not ROOMS[game_state["current_room"]]["puzzle"]:
        print("Загадок здесь нет.")
    else:
        print(ROOMS[game_state["current_room"]]["puzzle"][0])
        users_answer = input("Ваш ответ: ")
    
        if (users_answer.lower() == ROOMS[game_state["current_room"]]["puzzle"][1].lower() or ROOMS[game_state["current_room"]]["puzzle"][1] in NUMBERS and NUMBERS[ROOMS[game_state["current_room"]]["puzzle"][1]] == users_answer.lower()): # noqa: E501
            print("Загадка решена правильно!")
            ROOMS[game_state['current_room']]['puzzle'] = ()
          
            if game_state["current_room"] == "hall":
                game_state["player_inventory"].append("coin")
            
            elif game_state["current_room"] == "trap_room":
                game_state["player_inventory"].append("stick")
          
            elif game_state["current_room"] == "library":
                game_state["player_inventory"].append("big_book")
          
            print(f"Ваша награда: {game_state['player_inventory'][-1]}")
          
        else:
            
            if game_state["current_room"] == "trap_room":
                trigger_trap(game_state=game_state)
            
            else:
                print("Неверно. Попробуйте снова.")



# Функция попытки открытия сундука с сокровищами
def attempt_open_treasure(game_state: dict) -> None:
    '''
    game_state - текущее состояние игры
    '''
    if "treasure_key" in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
#        ROOMS[game_state["current_room"]]["items"].remove("treasure_chest")
        print(f"В сундуке сокровище! Вы победили за {game_state['steps_taken']} шагов!") # noqa: E501
        game_state["game_over"] = True

    else:
        users_answer = input("Сундук заперт. ... Ввести код? (да/нет) ")

        if users_answer.lower() == "да":
            users_code = input("Введние код: ")

            if users_code == ROOMS[game_state["current_room"]]["puzzle"][1]:
                print("Вы правильно вводите код, и замок щёлкает. Сундук открыт!")
                print(f"В сундуке сокровище! Вы победили за {game_state['steps_taken']} шагов!") # noqa: E501
                game_state["game_over"] = True

            else:
                print("Стены задрожали, весь замок ходит ходуном, где-то в стенах вы слышите: 'За дверью девять душ, твоя — следующая...'. Сундук остался заперт, попробуйте еще раз.") # noqa: E501

        else:
            print("Вы отступаете от сундука.")


# Функция склонения предметов
def get_subject_form_in_inventory(count: int) -> None:
    '''
    Склоняет слово "предмет" в зависимости от числа.
        ввод: Число.
        вывод: Склоненное слово "предмет".
    '''
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


# Функция генерации "случайных" чисел
def pseudo_random(seed: int, modulo: int) -> int:
    '''
    seed - количество шагов,
    modulo - целое число для определения диапазона результата
    '''
    rng_number = ma.sin(seed) * 12.9898 * 43758.5453
    rng_number_final = round((rng_number - ma.floor(rng_number)) * modulo)

    return rng_number_final

# Функция имитации срабатывания ловушки в комнате
def trigger_trap(game_state: dict) -> None:
    '''
    game_state - текущее состояние игры
    '''
    print("\nЛовушка активирована! Пол стал дрожать...")

    if len(game_state["player_inventory"]) > 0:
        rng_item_index = pseudo_random(seed=game_state["steps_taken"], modulo=len(game_state["player_inventory"])-1) # noqa: E501
        deleted_item = game_state["player_inventory"].pop(rng_item_index)
        print(f"Вы смогли выбраться, но в процессе потеряли {deleted_item}.")

    else:
        rng_damage = pseudo_random(seed=game_state["steps_taken"], modulo=TRAP_DMG_PROBABILITY) # noqa: E501

        if rng_damage < EVENT1_DEATH_DMG or game_state["steps_taken"] < 2:

            if "old_armor" in game_state["player_inventory"]:
                print("Вам повезло, что на вас были старые доспехи. Вы избежали смертельного урона.") # noqa: E501
                print("Ваши доспехи сломались.")
                game_state["player_inventory"].remove("old_armor")

            else: 
                print("Вы не успеваете увернуться, и на вас падает каменная плита. Игра окончена!") # noqa: E501
                game_state["game_over"] = True

        else:
            print("Вы успеваете увернуться от падающей плиты.")
            

# Функция случайных событий
def random_event(game_state: dict) -> None:
    '''
    game_state - текущее состояние игры
    '''
    rng_event_trigger = pseudo_random(seed=game_state["steps_taken"], modulo=EVENT_PROBABILITY) # noqa: E501

    if rng_event_trigger < EVENT_INTENSIVITY:
        rng_event_number = pseudo_random(seed=game_state["steps_taken"], modulo=EVENT_COUNT) # noqa: E501

        print("\nСобытие:")

        if rng_event_number == 0:
            print("Вы замечаете что-то блестящее на полу, это золотая монета (coin).")
            print("Вы подбираете монету.")
            game_state["player_inventory"].append("coin")

        elif rng_event_number == 1:

            print("Вы слышите шорох в темном углу комнаты. Ваш пульс заметно учащается.") # noqa: E501
            if "sword" in game_state["player_inventory"]:
                print("Вы обнажаете свой меч. Существо с гортанным рыком пятится назад и скрывается темноте.") # noqa: E501

            else:
                rng_damage_beast = pseudo_random(seed=game_state["steps_taken"], modulo=BEAST_DMG_PROBABILITY) # noqa: E501
                if rng_damage_beast < EVENT2_DEATH_DMG:

                    if "old_armor" in game_state["player_inventory"]:
                        print("Вам повезло, что на вас были старые доспехи. Существо когтями проходится по вашей броне и скрывается в темноте.") # noqa: E501
                        print("Ваши доспехи пришли в негодность.")
                        game_state["player_inventory"].remove("old_armor")

                    else: 
                        print("Существо прыгает на вас и наносит смертельную рану.")
                        print("Вы истекаете кровью на полу комнаты. Игра окончена")
                        game_state["game_over"] = True

                else:
                    print("Существо прыгает в вашу сторону, но вам везет, и оно промахивается.") # noqa: E501
                    print("После чего скрывается во тьме.")

        elif rng_event_number == 2:

            if game_state["current_room"] == "trap_room" and ("torch" not in game_state["player_inventory"]): # noqa: E501
                trigger_trap(game_state=game_state)

# Конец