import curses
import os
import time
from datetime import datetime
import sys
def message(msg):
        current_time = datetime.now()
        formatted_time = current_time.strftime('[%a %b %d %H:%M:%S %Y]')
        print(f"{formatted_time} {msg}")
def parse_line(line):
    """Parsuje řádky z index.cn pro komponenty."""
    parts = line.split('<')
    component = parts[0].strip()
    params = parts[1][:-1] if len(parts) > 1 else ""
    params = dict(param.split(':') for param in params.split() if ':' in param)
    return component, params

def draw_text(win, text, params):
    """Vykreslí text na základě parametrů a přidá box (rámeček) kolem textu."""
    backcolor = params.get('backcolor', 'BLACK')
    fontcolor = params.get('fontcolor', 'WHITE')
    placex = params.get('placex', 'CENTER')
    placey = params.get('placey', 'CENTER')
    border = params.get('border', 'FALSE') == 'TRUE'

    # Získání barev
    colors = {
        'BLACK': curses.COLOR_BLACK,
        'WHITE': curses.COLOR_WHITE,
        'RED': curses.COLOR_RED,
        'GREEN': curses.COLOR_GREEN,
        'YELLOW': curses.COLOR_YELLOW,
        'BLUE': curses.COLOR_BLUE,
        'MAGENTA': curses.COLOR_MAGENTA,
        'CYAN': curses.COLOR_CYAN
    }

    bg_color = colors.get(backcolor.upper(), curses.COLOR_BLACK)
    fg_color = colors.get(fontcolor.upper(), curses.COLOR_WHITE)

    # Získání pozice
    max_y, max_x = win.getmaxyx()
    x = max_x // 2 if placex == 'CENTER' else int(placex)
    y = max_y // 2 if placey == 'CENTER' else int(placey)

    # Nastavení barev pro text
    curses.init_pair(1, fg_color, bg_color)
    win.attron(curses.color_pair(1))

    if border:
        # Vytvoření borderu kolem textu (box)
        text_width = len(text)  # Šířka boxu je přesně podle délky textu
        text_height = 3  # Výška boxu (1 pro horní mez, 1 pro text, 1 pro dolní mez)

        # Kreslení horního okraje
        win.addstr(y - 1, x - text_width // 2, '┌' + '─' * text_width + '┐')

        # Kreslení textového řádku
        win.addstr(y, x - len(text) // 2, '│' + text + '│')

        # Kreslení dolního okraje
        win.addstr(y + 1, x - text_width // 2, '└' + '─' * text_width + '┘')
    else:
        # Vykreslení textu bez boxu
        win.addstr(y, x - len(text) // 2, text)

    win.attroff(curses.color_pair(1))

def draw_background(win, params):
    """Nastaví pozadí podle parametru backcolor."""
    backcolor = params.get('backcolor', 'BLACK')
    colors = {
        'BLACK': curses.COLOR_BLACK,
        'WHITE': curses.COLOR_WHITE,
        'RED': curses.COLOR_RED,
        'GREEN': curses.COLOR_GREEN,
        'YELLOW': curses.COLOR_YELLOW,
        'BLUE': curses.COLOR_BLUE,
        'MAGENTA': curses.COLOR_MAGENTA,
        'CYAN': curses.COLOR_CYAN
    }
    bg_color = colors.get(backcolor.upper(), curses.COLOR_BLACK)

    curses.init_pair(2, curses.COLOR_BLACK, bg_color)
    win.bkgd(' ', curses.color_pair(2))

def draw_title(win, text, params):
    """Zobrazí název stránky na vrchu."""
    fontcolor = params.get('fontcolor', 'WHITE')
    fg_color = {
        'WHITE': curses.COLOR_WHITE,
        'RED': curses.COLOR_RED,
        'GREEN': curses.COLOR_GREEN,
        'BLUE': curses.COLOR_BLUE
    }.get(fontcolor.upper(), curses.COLOR_WHITE)

    curses.init_pair(3, fg_color, curses.COLOR_BLACK)
    win.attron(curses.color_pair(3))
    win.addstr(0, 0, text)
    win.attroff(curses.color_pair(3))

def process_key_action(win, key, key_actions):
    """Zpracuje akci spojenou s klávesou."""
    if key == ord('d') and 'D' in key_actions:
        # Spustí akci pro klávesu 'D'
        action = key_actions['D']
        component, params = parse_line(action)
        if component.startswith('TEXT'):
            draw_text(win, component.split('.')[1], params)

def process_time_action(time_value):
    """Zpracuje akci TIME pro čekání daný čas."""
    try:
        wait_time = float(time_value)
        time.sleep(wait_time)
    except ValueError:
        message(f"Invalid time value: {time_value}")

def main_curses(stdscr):
    """Hlavní funkce pro vykreslení všech komponent."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    if len(sys.argv) > 1:
        if sys.argv[1] == "version":
            print(f"Rasmnout CN Engine 0.1.3 View")
        else:
            file = sys.argv[1]
            with open(f'{file}', 'r') as f:
                lines = f.readlines()
    else:
        message("Usage: cn-view <FILE>")

    key_actions = {}

    for line in lines:
        component, params = parse_line(line.strip())

        if component.startswith('TITLE'):
            draw_title(stdscr, component.split('.')[1], params)

        elif component.startswith('BACKGROUND'):
            draw_background(stdscr, params)

        elif component.startswith('KEY'):
            key_name = line.split('.')[1].strip()
            action = params.get('addManc', '')
            key_actions[key_name] = action

        elif component.startswith('TEXT'):
            draw_text(stdscr, component.split('.')[1], params)

        elif component.startswith('TIME'):
            time_value = line.split('<')[1][:-1]  # Vyjme čas z <time_value>
            process_time_action(time_value)

    # Čekání na klávesu
    stdscr.refresh()

    try:
        while True:
            key = stdscr.getch()

            # Zpracování akce podle klávesy
            process_key_action(stdscr, key, key_actions)

            if key == 27:  # ESC pro ukončení
                break

    except KeyboardInterrupt:
        # Ošetření CTRL+C pro ukončení aplikace
        curses.endwin()
        message("CTRL-C pressed, shutting down...")
        return

def main():
    curses.wrapper(main_curses)
