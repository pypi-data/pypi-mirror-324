import os
import sys

INSTALL_PATH = os.path.expanduser("~/.local/bin")

LAUNCHER_TEMPLATE = """#!/bin/bash
python3 "{script_path}" "$@"
"""

def register_app():
    script_path = os.path.abspath(sys.argv[0])
    script_name = os.path.splitext(os.path.basename(script_path))[0]

    os.makedirs(INSTALL_PATH, exist_ok=True)
    launcher_path = os.path.join(INSTALL_PATH, script_name)

    with open(launcher_path, "w") as f:
        f.write(LAUNCHER_TEMPLATE.format(script_path=script_path))

    os.chmod(launcher_path, 0o755)

    print(f"L'application '{script_name}' est enregistrée.")
    print(f"Vous pouvez maintenant l'exécuter en tapant '{script_name}' dans le terminal.")

def ensure_registered():
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    launcher_path = os.path.join(INSTALL_PATH, script_name)

    if not os.path.exists(launcher_path):
        register_app()
