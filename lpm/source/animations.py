import time
import itertools

# ~~~ Barra de carga conexion 
def animationBAR_barra():
    total = 20

    for i in range(total + 1):
        barra = "#" * i + "-" * (total - i)
        print(f"\r{' '*16}[{barra}] {i*5}%", end="", flush=True)
        time.sleep(0.2)

    print()


# ~~~ Barra de carga messagesUp
def animationsBAR_message(msg, msg_completed, num = 1):
    spinner = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")

    for _ in range(50):
        print(f"\r{' '*num}{msg} {next(spinner)}", end="", flush=True)
        time.sleep(0.1)

    print(f"\r{' '*num}{msg_completed}")



