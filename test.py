import keyboard

while True:
    print(sum(1 << i for i, c in enumerate("qaed")
              if keyboard.is_pressed(c)).to_bytes())
