"""Проверка полного прохождения и запретов на пропуск загадок."""

from contextlib import redirect_stdout
from io import StringIO

from game import handle_command, new_game


def run(game, command):
    with redirect_stdout(StringIO()):
        handle_command(game, command)


game = new_game()
run(game, "идти шлюз")
assert game["room"] == "склад"
run(game, "код 314")
assert "дверь открыта" not in game["done"]
run(game, "использовать фонарь")
assert "цифры найдены" not in game["done"]

for command in (
    "взять батарея",
    "использовать фонарь",
    "код 314",
    "идти шлюз",
):
    run(game, command)
assert game["room"] == "шлюз"

run(game, "взять провод")
assert "провод" not in game["inventory"]
run(game, "взять магнит")
run(game, "использовать магнит")
run(game, "взять провод")
run(game, "идти радиорубка")
assert game["room"] == "радиорубка"

run(game, "включить север")
assert not game["channels"]
run(game, "использовать провод")
run(game, "включить юг")
assert "юг" not in game["channels"]
run(game, "включить север")
run(game, "передать")
assert not game["won"]
run(game, "включить восток")
run(game, "передать")
assert game["won"]
print("Полное прохождение и ограничения проверены.")
