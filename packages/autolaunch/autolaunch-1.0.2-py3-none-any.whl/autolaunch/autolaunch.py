import os
import subprocess
import sys
import logging
import ctypes

# 📜 Configuration des logs
LOG_FILE = "autolaunch.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# 📦 Dépendances nécessaires
REQUIRED_LIBRARIES = ["setuptools", "wheel", "twine"]

def install_missing_packages():
    """Installe automatiquement les dépendances manquantes."""
    for package in REQUIRED_LIBRARIES:
        try:
            __import__(package)  # Vérifie si la lib est installée
        except ImportError:
            print(f"📦 Installation de '{package}' en cours...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"✅ '{package}' installé avec succès.")
            logging.info(f"✅ '{package}' installé avec succès.")

install_missing_packages()

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
    """Enregistre une variable d'environnement de manière persistante avec logs."""
    
    # Vérifier si on est admin
    if not is_admin():
        logging.error("❌ Python n'est pas exécuté avec les droits administrateurs.")
        print("Erreur : Veuillez exécuter Python en tant qu'administrateur.")
        return

    # Vérifier si la variable est déjà enregistrée
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

def ensure_registered(app_name="MON_APP", app_path=None):
    """Enregistre l'application si elle n'est pas déjà enregistrée."""
    if app_path is None:
        app_path = os.path.abspath(sys.argv[0])  # Obtient le chemin actuel du script

    set_env_variable(app_name, app_path)

def unregister_app(app_name="MON_APP"):
    """Supprime une application enregistrée."""
    try:
        subprocess.run(f'reg delete HKCU\\Environment /F /V {app_name}', shell=True, check=True)
        logging.info(f"❌ Variable '{app_name}' supprimée.")
        print(f"❌ Variable '{app_name}' supprimée.")
    except subprocess.CalledProcessError as e:
        logging.error(f"⚠️ Erreur lors de la suppression de '{app_name}': {e}")
        print(f"⚠️ Impossible de supprimer '{app_name}', voir les logs.")

# 📌 Exemple d'utilisation
if __name__ == "__main__":
    ensure_registered()
