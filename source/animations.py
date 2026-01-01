import sys
import time
import itertools

# ~~ modulos internos lpm ~~
from source.modules.load_config import load_config, check_newVersion


# ~~~ funciones principales de animacion ~~~

def icon():
    config_json = load_config()
    info_newVersion = check_newVersion()

    icon = config_json["info"]["icon"]

    if (info_newVersion != False):
        icon[1] += info_newVersion

    for i in config_json["info"]["icon"]:
        print(i)


def bar_animation(num, msg):
    for i in range(20 + 1):
        barra = "█" * i + "-" * (20 - i)
        print(f"\r{' '*num}{msg}[{barra}] {i*5}%", end="", flush=True)
        time.sleep(0.2)
    print()


def message_animation(msg, msg_completed, duration = 2.0, num = 1):
    spinner = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
    end_time = time.time() + duration
    indent = " " * num

    while time.time() < end_time:
        sys.stdout.write(f"\r\033[K{indent}{msg} {next(spinner)}")
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write(f"\r\033[K{indent}{msg_completed}\n")
    sys.stdout.flush()
