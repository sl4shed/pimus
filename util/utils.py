from lib import lcd
import time


def draw_centered_text(screen: lcd.Screen, text, row):
    if len(text) > screen.columns:
        return

    spacing = (screen.columns - len(text)) / 2
    screen.set_cursor(spacing, row)
    screen.write_string(text)


def draw_scrolling_text(screen, text, row, scroll=0):
    width = screen.columns
    padded_text = text + " " * width
    scroll = scroll % len(padded_text)

    visible = padded_text[scroll : scroll + width]

    if len(visible) < width:
        visible += padded_text[: width - len(visible)]

    screen.set_cursor(0, row)
    screen.write_string(visible)


def millis():
    return int(time.monotonic() * 1000)
