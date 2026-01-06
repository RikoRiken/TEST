from security import crypto
from file_io import manager

AUTH_FILENAME = "auth.crypt"

def est_inscrit() -> bool:
    """Vérifie si le compte Root existe déjà."""
    # On essaie simplement de lire le fichier auth.crypt
    return manager.lire_fichier_binaire(AUTH_FILENAME) is not None

def inscrire_root(password: str) -> bool:
    """Initialise le compte Root."""
    try:
        cle_derivee, sel = crypto.deriver_cle(password)
        data = sel + cle_derivee
        return manager.ecrire_fichier_binaire(AUTH_FILENAME, data)
    except Exception as e:
        print(f"Erreur inscription : {e}")
        return False

def verifier_root(password: str) -> bool:
    """Vérifie si le mot de passe est celui du Root."""
    data = manager.lire_fichier_binaire(AUTH_FILENAME)
    
    if not data or len(data) < 48:
        return False

    sel_stocke = data[:16]
    hash_stocke = data[16:]

    cle_calculee, _ = crypto.deriver_cle(password, sel=sel_stocke)
    return cle_calculee == hash_stocke