import curses
import socket
import ssl
import curses
import os
import time
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
        print(f"Invalid time value: {time_value}")
def send_request(protocol, ip, path):
    try:
        if protocol == 'cn' or protocol == 'cnss':
            # Nastavení portu podle protokolu
            port = 60000 if protocol == 'cn' else 61000

            # Pokud používáme SSL (cnss), použijeme SSL socket
            if protocol == 'cnss':
                context = ssl.create_default_context()
                with socket.create_connection((ip, port)) as sock:
                    with context.wrap_socket(sock, server_hostname=ip) as secure_sock:
                        secure_sock.send(f"{protocol}:GET:/{path}".encode())
                        response = secure_sock.recv(4096).decode()
            else:
                with socket.create_connection((ip, port)) as sock:
                    sock.send(f"{protocol}:GET:/{path}".encode())
                    response = sock.recv(4096).decode()

        elif protocol == 'cnf':
            port = 62000  # Pro cnf používáme port 62000
            with socket.create_connection((ip, port)) as sock:
                sock.send(f"{protocol}:GET:/{path}".encode())
                response = sock.recv(4096).decode()

        return response
    except Exception as e:
        return f"Chyba při připojování: {e}"

def main_curses(stdscr):
    # Inicializace barev
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Černý text na bílém pozadí
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Bílý text na černém pozadí
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Pro logo (černý text na bílém pozadí)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Pro vstupní pole (bílý text na černém pozadí)

    # Nastavíme pozadí na bílou
    stdscr.bkgd(' ', curses.color_pair(1))  # Bílý background s černým textem
    stdscr.clear()

    # Získáme velikost obrazovky
    max_y, max_x = stdscr.getmaxyx()

    # Logo
    logo = '''▄█▄       ▄      ▄▄▄▄▄   ▄███▄   ██   █▄▄▄▄ ▄█▄     ▄  █
█▀ ▀▄      █    █     ▀▄ █▀   ▀  █ █  █  ▄▀ █▀ ▀▄  █   █
█   ▀  ██   █ ▄  ▀▀▀▀▄   ██▄▄    █▄▄█ █▀▀▌  █   ▀  ██▀▀█
█▄  ▄▀ █ █  █  ▀▄▄▄▄▀    █▄   ▄▀ █  █ █  █  █▄  ▄▀ █   █
▀███▀  █  █ █            ▀███▀      █   █   ▀███▀     █
       █   ██                      █   ▀             ▀'''

    # Zobrazíme logo na střed obrazovky s bílým pozadím a černým textem
    logo_y = max_y // 4  # Umístíme logo do čtvrtiny obrazovky
    for i, line in enumerate(logo.splitlines()):
        if logo_y + i < max_y:
            stdscr.addstr(logo_y + i, (max_x - len(line)) // 2, line, curses.color_pair(3))

    # Získáme URL od uživatele
    input_y = logo_y + len(logo.splitlines()) + 2  # Vstup pod logem
    input_x = (max_x // 2) - 30  # Pozice pro vstupní pole (60 znaků)

    # Připravíme místo pro uživatelský vstup
    curses.echo()
    stdscr.addstr(input_y - 1, input_x, "CN Server", curses.color_pair(2))
    stdscr.move(input_y, input_x)  # Přesuneme kurzor do správné pozice

    # Změníme barvy pro vstupní pole (bílý text na černém pozadí)
    stdscr.attron(curses.color_pair(4))

    # Zde se již nezobrazuje čárka
    input_url = stdscr.getstr(input_y, input_x, 60).decode('utf-8')  # Maximálně 60 znaků

    # Resetování barev po zadání
    stdscr.attroff(curses.color_pair(4))

    # Zpracování URL
    if input_url.startswith("cn://"):
        protocol = "cn"
        ip_and_path = input_url[5:]
    elif input_url.startswith("cnss://"):
        protocol = "cnss"
        ip_and_path = input_url[7:]
    elif input_url.startswith("cnf://"):
        protocol = "cnf"
        ip_and_path = input_url[6:]
    else:
        stdscr.addstr(max_y - 1, 0, "Neplatný protokol. Použijte cn://, cnss:// nebo cnf://.", curses.color_pair(2))
        stdscr.getch()
        return

    # Rozdělení IP a cesty
    if "/" in ip_and_path:
        ip, path = ip_and_path.split("/", 1)
    else:
        ip, path = ip_and_path, "index.cn"
    response = send_request(protocol, ip, path)
    stdscr.clear()
    key_actions = {}
    for i, line in enumerate(response.splitlines()):
        if i + 1 < max_y:
            line = line[:max_x-1]
            if line == "Error 404":
                line = f"Error 404\n     {path}: Not Found "
                stdscr.addstr(i + 1, 0, line)
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
                time_value = line.split('<')[1][:-1]
                process_time_action(time_value)
    stdscr.refresh()
    try:
        while True:
            key = stdscr.getch()
            process_key_action(stdscr, key, key_actions)
            if key == 27:
                break
    except KeyboardInterrupt:
        curses.endwin()
        return

    stdscr.getch()
def main():
    curses.wrapper(main_curses)
