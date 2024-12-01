import logging
import os
from datetime import datetime
import inspect


def setup_logger():
    """
    Configure un logger pour le module appelant.
    - Si le module est exécuté directement, crée un fichier dédié.
    - Si le module est importé, utilise le logger du script principal.
    """
    # Obtenir le module appelant réel en inspectant la pile d'appels
    frame = inspect.currentframe().f_back
    while frame:
        module_name = frame.f_globals["__name__"]
        if module_name != "runpy" and module_name != "__main__":
            break
        frame = frame.f_back
    else:
        module_name = "__main__"  # Cas où aucun autre module n'est trouvé

    # Vérifier si un logger pour ce module existe déjà
    if logging.getLogger(module_name).handlers:
        return logging.getLogger(module_name)

    # Créer un dossier spécifique pour les logs
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas

    # Construire un nom de fichier dynamique basé sur le module et la date/heure
    if module_name == "__main__":
        # Nom de fichier pour le script principal
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_name = f"{module_name}_{current_time}.log"
    else:
        # Pas de fichier dédié pour les modules importés
        log_file_name = None

    # Configurer le logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # Niveau de log

    # Crée un gestionnaire pour le fichier si applicable
    if log_file_name:
        log_file_path = os.path.join(log_dir, log_file_name)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # # Crée un gestionnaire pour la console
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)
    # console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # console_handler.setFormatter(console_formatter)
    # logger.addHandler(console_handler)

    return logger
