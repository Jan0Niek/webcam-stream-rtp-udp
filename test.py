import keyboard

while True:
    sum(1 << i if keyboard.is_pressed(c) else 0 for i, c in enumerate("qaed"))
