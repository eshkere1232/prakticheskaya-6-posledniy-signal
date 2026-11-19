"""«Последний сигнал» — текстовая игра о спасении полярной станции."""

ROOMS = {
    "склад": {
        "position": (0, 0),
        "title": "Склад станции",
        "story": (
            "Буря обесточила станцию. За дверью лежит путь к радиорубке. "
            "На складе стоит ящик с батареей, а на двери светится замок."
        ),
        "items": ["батарея"],
        "exit": "шлюз",
    },
    "шлюз": {
        "position": (1, 0),
        "title": "Шлюз с дроном",
        "story": (
            "Охранный дрон кружит над проводом. Рядом лежит магнит. "
            "Без провода антенну в радиорубке не починить."
        ),
        "items": ["магнит", "провод"],
        "exit": "радиорубка",
    },
    "радиорубка": {
        "position": (2, 0),
        "title": "Радиорубка",
        "story": (
            "Антенна повреждена. Табличка гласит: «Для сигнала включи "
            "северный и восточный каналы. Южный перегружен»."
        ),
        "items": [],
        "exit": None,
    },
}

ITEMS = {
    "фонарь": "Показывает скрытые цифры, если вставлена батарея.",
    "батарея": "Питание для фонаря.",
    "магнит": "Может отвлечь охранный дрон.",
    "провод": "Нужен для ремонта антенны.",
}

HELP = (
    "Команды: осмотреться, взять <предмет>, использовать <предмет>, "
    "код <число>, идти <комната>, включить <канал>, передать, "
    "инвентарь, карта, подсказка, помощь, выход."
)


def new_game():
    """Создать независимое состояние для новой игры."""
    return {
        "room": "склад",
        "inventory": ["фонарь"],
        "done": set(),
        "channels": set(),
        "won": False,
    }


def describe(game):
    room = ROOMS[game["room"]]
    print(f"\n=== {room['title']} ===")
    print(room["story"])
    visible = []
    for item in room["items"]:
        if item in game["inventory"]:
            continue
        if item == "провод" and "дрон отвлечён" not in game["done"]:
            print("Провод виден, но дрон не подпускает к нему.")
        else:
            visible.append(item)
    if visible:
        print("Можно взять:", ", ".join(visible))
    if room["exit"]:
        print("Дальше:", room["exit"])


def show_inventory(game):
    print("\nИнвентарь:")
    for item in game["inventory"]:
        print(f"- {item}: {ITEMS[item]}")


def show_map(game):
    print("Карта станции (координаты неизменны):")
    for name, room in ROOMS.items():
        mark = " <- вы здесь" if name == game["room"] else ""
        print(f"{room['position']}: {name}{mark}")


def give_hint(game):
    room = game["room"]
    if room == "склад":
        if "цифры найдены" not in game["done"]:
            print("Найди питание для фонаря и используй фонарь.")
        else:
            print("Введи найденные цифры командой «код 314».")
    elif room == "шлюз":
        if "дрон отвлечён" not in game["done"]:
            print("Возьми магнит и используй его против дрона.")
        else:
            print("Теперь можно взять провод и идти в радиорубку.")
    else:
        print("Почини антенну проводом, включи север и восток, затем передай сигнал.")


def take_item(game, item):
    room = ROOMS[game["room"]]
    if not item:
        print("Укажи предмет: взять <предмет>.")
        return
    if item in game["inventory"]:
        print("Этот предмет уже в инвентаре.")
        return
    if item not in room["items"]:
        print("Здесь нет такого предмета.")
        return
    if item == "провод" and "дрон отвлечён" not in game["done"]:
        print("Дрон преграждает путь к проводу!")
        return
    game["inventory"].append(item)
    print(f"Предмет «{item}» добавлен в инвентарь.")


def use_item(game, item):
    if not item:
        print("Укажи предмет: использовать <предмет>.")
        return
    if item not in game["inventory"]:
        print("Такого предмета нет в инвентаре.")
        return
    room = game["room"]
    if room == "склад" and item == "фонарь":
        if "батарея" not in game["inventory"]:
            print("Фонарь не работает. Нужна батарея.")
        else:
            game["done"].add("цифры найдены")
            print("На стене проявились цифры: 314.")
    elif room == "шлюз" and item == "магнит":
        game["done"].add("дрон отвлечён")
        print("Дрон прилип к магнитной панели. Путь к проводу свободен.")
    elif room == "радиорубка" and item == "провод":
        game["done"].add("антенна починена")
        print("Ты восстановил проводку антенны.")
    else:
        print("Здесь этот предмет не помогает.")


def enter_code(game, code):
    if game["room"] != "склад":
        print("Здесь нет кодового замка.")
    elif "цифры найдены" not in game["done"]:
        print("Сначала найди подсказку к замку.")
    elif code == "314":
        game["done"].add("дверь открыта")
        print("Замок щёлкнул. Путь в шлюз открыт!")
    else:
        print("Неверный код. Замок остался закрыт.")


def go_to(game, destination):
    room = game["room"]
    if destination != ROOMS[room]["exit"]:
        print("Отсюда нельзя пройти в эту комнату.")
    elif room == "склад" and "дверь открыта" not in game["done"]:
        print("Дверь заперта. Найди код.")
    elif room == "шлюз" and "провод" not in game["inventory"]:
        print("Для ремонта антенны сначала возьми провод.")
    else:
        game["room"] = destination
        describe(game)


def switch_channel(game, channel):
    if game["room"] != "радиорубка":
        print("Панель каналов находится в радиорубке.")
    elif "антенна починена" not in game["done"]:
        print("Сначала почини антенну.")
    elif channel not in {"север", "восток", "юг"}:
        print("Доступные каналы: север, восток, юг.")
    elif channel == "юг":
        print("Южный канал перегружен. Ты не включаешь его.")
    elif channel in game["channels"]:
        print("Этот канал уже включён.")
    else:
        game["channels"].add(channel)
        print(f"Канал «{channel}» включён.")


def transmit(game):
    if game["room"] != "радиорубка":
        print("Передатчик находится в радиорубке.")
    elif "антенна починена" not in game["done"]:
        print("Антенна ещё не починена.")
    elif game["channels"] != {"север", "восток"}:
        print("Сигнал слабый. Нужны северный и восточный каналы.")
    else:
        game["won"] = True
        print("\nСигнал дошёл до спасателей! Станция спасена. Победа!")


def handle_command(game, command):
    action, _, argument = command.partition(" ")
    argument = argument.strip()
    if action == "осмотреться":
        describe(game)
    elif action == "инвентарь":
        show_inventory(game)
    elif action == "карта":
        show_map(game)
    elif action == "подсказка":
        give_hint(game)
    elif action == "помощь":
        print(HELP)
    elif action == "взять":
        take_item(game, argument)
    elif action == "использовать":
        use_item(game, argument)
    elif action == "код":
        enter_code(game, argument)
    elif action == "идти":
        go_to(game, argument)
    elif action == "включить":
        switch_channel(game, argument)
    elif action == "передать":
        transmit(game)
    else:
        print("Неизвестная команда. Введи «помощь».")


def main():
    game = new_game()
    print("ПОСЛЕДНИЙ СИГНАЛ")
    print("У тебя одна ночь, чтобы восстановить связь с полярной станции.")
    print(HELP)
    describe(game)
    while not game["won"]:
        try:
            command = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nИгра завершена.")
            break
        if command == "выход":
            print("Игра завершена.")
            break
        if not command:
            print("Введи команду или «помощь».")
            continue
        handle_command(game, command)


if __name__ == "__main__":
    main()
