import os
import sys
import subprocess
import logging
import ctypes

# 📜 Configuration des logs
logging.basicConfig(
    filename="autolaunch.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def is_admin():
    """Vérifie si le script est exécuté en tant qu'administrateur."""
    try:
        return os.getuid() == 0  # UNIX/Linux
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0  # Windows

def check_env_variable(name):
    """Vérifie si une variable d'environnement est déjà définie."""
    value = os.environ.get(name)
    if value:
        logging.info(f"🔍 Variable '{name}' trouvée : {value}")
        return value
    else:
        logging.warning(f"⚠️ Variable '{name}' non trouvée.")
        return None

def set_env_variable(name, value):
    """Ajoute une variable d'environnement de manière persistante."""
    if not is_admin():
        logging.error("❌ Python n'est pas exécuté avec les droits administrateurs.")
        print("Erreur : Veuillez exécuter Python en mode administrateur.")
        return
    
    # Vérifier si la variable existe déjà
    if check_env_variable(name):
        logging.info(f"✅ La variable '{name}' est déjà définie.")
        return

    try:
        subprocess.run(f'setx {name} "{value}"', shell=True, check=True)
        logging.info(f"✅ Variable '{name}' enregistrée avec succès : {value}")
        print(f"✅ Variable '{name}' enregistrée avec succès.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Erreur lors de l'enregistrement de '{name}': {e}")
        print(f"Erreur lors de l'ajout de '{name}', voir les logs.")

def create_executable_command(app_name, app_path):
    """Crée un fichier .cmd exécutable pour lancer l'application."""
    cmd_path = os.path.join(os.environ["USERPROFILE"], f"{app_name}.cmd")
    
    with open(cmd_path, "w") as f:
        f.write(f'@echo off\npython "{app_path}" %*\n')

    logging.info(f"✅ Fichier exécutable créé : {cmd_path}")
    print(f"✅ Fichier exécutable ajouté : {cmd_path}")

def ensure_registered():
    """Enregistre l'application et la rend exécutable depuis n'importe où."""
    app_path = os.path.abspath(sys.argv[0])  # Chemin du script actuel
    app_name = os.path.splitext(os.path.basename(app_path))[0]  # Nom du script sans extension

    # Vérifier si admin
    if not is_admin():
        logging.error("❌ Python n'est pas exécuté en administrateur.")
        print("Erreur : Exécute ce script en mode administrateur.")
        return

    # Enregistre la variable d’environnement
    set_env_variable(app_name, app_path)
    
    # Crée une commande exécutable
    create_executable_command(app_name, app_path)

    print(f"✅ '{app_name}' peut maintenant être lancé depuis n'importe où.")

def unregister_app():
    """Supprime l'application enregistrée."""
    app_path = os.path.abspath(sys.argv[0])  # Chemin du script actuel
    app_name = os.path.splitext(os.path.basename(app_path))[0]  # Nom du script sans extension

    try:
        subprocess.run(f'reg delete HKCU\\Environment /F /V {app_name}', shell=True, check=True)
        logging.info(f"❌ Variable '{app_name}' supprimée.")
        print(f"❌ Variable '{app_name}' supprimée.")

        cmd_path = os.path.join(os.environ["USERPROFILE"], f"{app_name}.cmd")
        if os.path.exists(cmd_path):
            os.remove(cmd_path)
            logging.info(f"🗑️ Fichier exécutable supprimé : {cmd_path}")
            print(f"🗑️ Fichier exécutable supprimé : {cmd_path}")

    except subprocess.CalledProcessError as e:
        logging.error(f"⚠️ Erreur lors de la suppression de '{app_name}': {e}")
        print(f"⚠️ Impossible de supprimer '{app_name}', voir les logs.")

def register_app(app_name, app_path):
    """Alias de `ensure_registered` pour plus de clarté."""
    ensure_registered()

# 📌 Exemple d'utilisation
if __name__ == "__main__":
    if "--unregister" in sys.argv:
        unregister_app()
    else:
        ensure_registered()
