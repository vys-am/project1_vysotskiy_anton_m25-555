# labyrinth_game/player_actions.py

# Обозначаем куда смотреть внутри наших файлов
from .constants import ROOMS
from .utils import (
    describe_current_room,
    get_subject_form_in_inventory,
    random_event,
)


#Создаем функцию отображения инвентаря
def show_inventory(game_state: dict) -> None:
    '''
    game_state - текущее состояние игры
    Показывает что в инвентаре у игрока (пусто или нет)
    '''
    len_inventory = len(game_state["player_inventory"])
    if not game_state["player_inventory"]:
        print("Предметов в инвентаре нет.")
    else:
        formatted_string = " & ".join(game_state["player_inventory"])
        print(f"В инвентаре лежит {len_inventory} {get_subject_form_in_inventory(len_inventory)}  \n== {formatted_string.upper()} ==") # noqa: E501

# Функция получения ввода с клавиатуры
def get_input(prompt="\n> ") -> str:
    '''
    promt - как будет отображаться строка ввода пользователя
    '''
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    
# Функция движения игрока
def move_player(game_state: dict, direction: str) -> None:
    '''
    game_state - текущее состояние игры
    Функция позволяющая перемещаться по игровому миру
    '''
    if direction not in ROOMS[game_state["current_room"]]["exits"]:
        # Если выхода в этом направлении нет
        print("Нельзя пойти в этом направлении.")
    else:
        
        if ROOMS[game_state["current_room"]]["exits"][direction] == "treasure_room":
            
            if "rusty_key" in game_state["player_inventory"]:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.") # noqa: E501
                game_state["current_room"] = ROOMS[game_state["current_room"]]["exits"][direction] # noqa: E501
                game_state["steps_taken"] += 1
                describe_current_room(game_state=game_state)

            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        
        else:
            game_state["current_room"] = ROOMS[game_state["current_room"]]["exits"][direction] # noqa: E501
            game_state["steps_taken"] += 1
            describe_current_room(game_state=game_state)
    
        random_event(game_state=game_state)

# Функция подбора предмета в комнате
def take_item(game_state: dict, item_name: str) -> None:
    '''
    game_state - текущее состояние игры
    item_name - название предмета
    Функция позволяющая поднимать предметы, если они есть в комнате
    '''
    if item_name not in ROOMS[game_state["current_room"]]["items"]:
        # Если предмета нет
        print("Такого предмета здесь нет.")
        
    else:
        # print("В комнате есть эти предметы")
        
        # Обновляем состояние игры, добавляем предмет в инвентарь
        game_state["player_inventory"].append(item_name)
        # print(game_state)

        # Найти индекс предмета 
        need_to_del_item_from_room = ROOMS[game_state["current_room"]]["items"].index(item_name) # noqa: E501
        
        # Удаляем предмет по индексу
        ROOMS[game_state["current_room"]]["items"].pop(need_to_del_item_from_room)

        # Напечатайте сообщение о том, что игрок подобрал предмет("Вы подняли:").
        print(f"Вы подняли: {item_name}")
        
# Функция для использования предмета из инвентаря
def use_item(game_state: dict, item_name: str) -> None:
    '''
    game_state - текущее состояние игры
    item_name - название предмета
    Функция позволяющая использовать предметы, если они есть в инвентаре
    '''
    check_inventory = game_state["player_inventory"]
    bbox_list = ["bronze_box", "bronze box"]
    
    if item_name not in check_inventory:
        print("У вас нет такого предмета.")
    else:
        if item_name == "torch":
            print("Вокруг стало светлее.")
        elif item_name == "sword":
            print("Вы изрекаете клич: 'За короля! За королевство!'. Ваша уверенность выросла!") # noqa: E501
        elif item_name in bbox_list:
            # Удалить из инвентаря этот предмет + добавить предмет rusty_key
            # Найти индекс предмета 
            indices = min([i for i, x in enumerate(game_state["player_inventory"]) if x in bbox_list]) # noqa: E501
            # Удалить предмет по индексу 
            game_state["player_inventory"].pop(indices)
            # Добавить ключ в инвентарь
            game_state["player_inventory"].append("rusty_key")
            # По сути, тут можно было сделать замену (но мне кажется так правильнее)
            
            # Вывести сообщение
            print("Бокс исчез из вашего инвентаря, но вы получили ключ!")
        else: 
            print("Я не знаю как это использовать.")
            
# Конец