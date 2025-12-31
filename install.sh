#!/bin/sh
set -e

INSTALL_DIR="$HOME/.lpm/program"
BIN_DIR="$HOME/.local/bin"

echo "[lpm] packages administrator"


if ! command -v python3 >/dev/null 2>&1;
then
    echo "[ ERROR ] python3 no esta instalado."
    exit 1
fi

echo ""

mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

echo "instalando..."
cp -r source "$INSTALL_DIR/"
cp lpm.py "$INSTALL_DIR/"

python3 -m venv "$INSTALL_DIR/lpm_venv"
. "$INSTALL_DIR/lpm_venv/bin/activate"

pip install --upgrade pip
pip install requests


cat > "$BIN_DIR/lpm" <<EOF
#!/bin/sh
. "$INSTALL_DIR/lpm_venv/bin/activate"
exec python "$INSTALL_DIR/lpm.py"
"\$@"
EOF

chmod +x "$BIN_DIR/lpm"

echo
echo "[ OK ] Instalacion Completada.."