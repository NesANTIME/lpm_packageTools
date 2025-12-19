import sys
import time
import itertools

# ~~~ Barra de carga conexion 
def animationBAR_barra(num, msg = ""):
    total = 20
    indent = " " * num

    for i in range(total + 1):
        barra = "█" * i + "-" * (total - i)
        print(f"\r{indent}{msg}[{barra}] {i*5}%", end="", flush=True)
        time.sleep(0.2)

    print()


# ~~~ Barra de carga messagesUp
def animationsBAR_message(msg, msg_completed, duration = 2.0, num = 1):
    spinner = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
    end_time = time.time() + duration
    indent = " " * num

    while time.time() < end_time:
        sys.stdout.write(f"\r\033[K{indent}{msg} {next(spinner)}")
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write(f"\r\033[K{indent}{msg_completed}\n")
    sys.stdout.flush()




