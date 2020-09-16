import time
import digitalio
from digitalio import Direction, Pull
import board

cols = [digitalio.DigitalInOut(x) for x in (board.D16, board.D12, board.D20)]
rows = [digitalio.DigitalInOut(x) for x in (board.D18, board.D23, board.D24, board.D25)]


keys = (('1', '2', '3'),
        ('4', '5', '6'),
        ('7', '8', '9'),
        ('*', 0, '#'))


while True:
    pressed = ''
    for pin in rows+cols:
        pin.direction = Direction.INPUT
        pin.pull = Pull.UP
    for row in range(len(rows)):
        rows[row].direction = Direction.OUTPUT
        rows[row].value = False
        for col in range(len(cols)):
            if not cols[col].value:
                pressed = keys[row][col]
        rows[row].direction = Direction.INPUT
        rows[row].pull = Pull.UP
    if(pressed != ''):
        print(pressed)
    time.sleep(0.22)