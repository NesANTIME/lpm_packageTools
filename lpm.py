import argparse

# ~~ modulos internos lpm ~~
from source.animations import icon
from source.logic import verify_credentials, lpm_upgrade, lpm_version


# ~~~ funciones ~~~

def install(args):
    icon()
    verify_credentials("install", args.package)

def search(args):
    icon()
    verify_credentials("search", args.package)

def list(args):
    icon()
    verify_credentials("list", None)

def update(args):
    icon()
    verify_credentials("update", None)

def use(args):
    verify_credentials("use", [args.package, args.args_script])


#def delivery_remove(args):
#    print(f"Desinstalando el paquete {args.name}...")

#def delivery_config():
#    print("En Desarrollo")


parser = argparse.ArgumentParser(
    prog="lpm",
    description="Administrador de paquetes privado hecho por NesAnTime."
)
parser.add_argument('--upgrade', action='store_true', help='[!] Actualizar lpm desde el repositorio!')
parser.add_argument('--version', action='store_true', help='[!] Mostrar version LPM!')

subparsers = parser.add_subparsers(dest="command")

    # lpm install <paquete>
install_parser = subparsers.add_parser("install", help="[!] Instala un paquete.")
install_parser.add_argument("package")
install_parser.set_defaults(func=install)

    # lpm update <paquete>
search_parser = subparsers.add_parser("search", help="[!] Busca un paquete.")
search_parser.add_argument("package")
search_parser.set_defaults(func=search)

    # lpm use <paquete>
use_parser = subparsers.add_parser("use", help="[!] Ejecuta un paquete.")
use_parser.add_argument("package")
use_parser.add_argument('args_script', nargs=argparse.REMAINDER, help='Argumentos del ejecutable')
use_parser.set_defaults(func=use)

    # lpm remove <paquete>
    #remove_parser = subparsers.add_parser("remove", help="[!] Desinstalar un paquete.")
    #remove_parser.add_argument("name")
    #remove_parser.set_defaults(func=delivery_remove)

    # lpm list
list_parser = subparsers.add_parser("list", help="[!] Listar los paquetes instalados.")
list_parser.set_defaults(func=list)

    # lpm update
update_parser = subparsers.add_parser("update", help="[!] Actualizar todos los paquetes instalados.")
update_parser.set_defaults(func=update)

args = parser.parse_args()

if args.version:
    icon()
    lpm_version()
    exit(0)

if args.upgrade:
    icon()
    lpm_upgrade()
    exit(0)

        
if (hasattr(args, "func")):
    args.func(args)
else:
    icon()
    parser.print_help()
